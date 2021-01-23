import os
import sys
from pathlib import Path
from typing import Dict, List
from urllib3.poolmanager import PoolManager
from urllib3.response import HTTPResponse

from github import Github
from github.GitRelease import GitRelease
from github.Repository import Repository

from mkdocs_markmap.__meta__ import PACKAGE_NAME, PROJECT_NAME, PROJECT_VERSION, REPOSITORY


PROJECT_PATH: Path = Path(__file__).parent.parent.parent.absolute()
DIST_PATH: Path = PROJECT_PATH / 'dist'
CHANGELOG_PATH: Path = PROJECT_PATH / 'changelog'

GZ_WILDCARD: str = f'{PROJECT_NAME}-{PROJECT_VERSION}*.gz'
WHL_WILDCARD: str = f'{PACKAGE_NAME}-{PROJECT_VERSION}*.whl'


class GithubHandler(object):
    def __init__(self, tag: str) -> None:
        self.tag = tag
        github_token = os.environ.get('GITHUB_TOKEN')
        if github_token is None:
            print('environment variable "GITHUB_TOKEN" is not set')
            sys.exit(1)
        self.github: Github = Github(github_token)
        self.repository: Repository = self.github.get_repo(REPOSITORY)


class AssetCollector(object):
    def get_assets(self) -> List[str]:
        gz_assets: List[str] = list(str(p) for p in DIST_PATH.glob(GZ_WILDCARD))
        whl_assets: List[str] = list(str(p) for p in DIST_PATH.glob(WHL_WILDCARD))

        assert len(gz_assets) == 1, \
            f'release asset "{GZ_WILDCARD}" is missing in {self.dist_path}: run "inv build" first'
        assert len(whl_assets) == 1, \
            f'release asset "{WHL_WILDCARD}" is missing in {self.dist_path}: run "inv build" first'

        return gz_assets + whl_assets


class AssetDownloader(GithubHandler):
    def get_assets_from_release(self) -> List[str]:
        try:
            release: GitRelease = next(r for r in self.repository.get_releases() if r.tag_name == self.tag)
        except StopIteration:
            print(f'Release "{self.tag}" does not exist')
            sys.exit(1)
        
        DIST_PATH.mkdir(exist_ok=True)
        assets = []

        http: PoolManager = PoolManager()
        for asset in release.get_assets():
            response: HTTPResponse = http.request('GET', asset.browser_download_url)
            if response.status != 200:
                print(f'Download of asset "{asset.name}" failed: {asset.browser_download_url} ({response.status})')
                sys.exit(1)

            file_path: Path = DIST_PATH / asset.name
            with open(file_path, 'wb') as fp:
                fp.write(response.data)
            
            assets.append(str(file_path))
        
        return assets


class ChangelogLoader:
    def __init__(self, changelog_path: Path = CHANGELOG_PATH) -> None:
        self._changelog_path = changelog_path
    
    def _drop_headline(self, content: str) -> str:
        headline_detected: bool = False
        text_started: bool = False

        lines = []
        for line in content.split('\n'):
            if not headline_detected and line.strip().startswith('#'):
                headline_detected = True
                continue

            if not text_started:
                if line.strip() == '':
                    continue

                if headline_detected:
                    text_started = True
            
            lines.append(line)

        while lines[-1] == '':
            lines.pop()
        
        return '\n'.join(lines)

    def get(self, release: str, drop_headline: bool = True) -> str:
        try:
            with open(self._changelog_path / f'{release}.md', 'r') as fp:
                content = fp.read()

            if drop_headline:
                content = self._drop_headline(content)
            
            return content
        
        except OSError as e:
            print(f'unable to load changelog for release {release}: {e}')
            sys.exit(1)
