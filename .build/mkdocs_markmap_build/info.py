import json
from typing import Dict, List
from urllib3.poolmanager import PoolManager
from urllib3.response import HTTPResponse

from github.GitRelease import GitRelease

from mkdocs_markmap.__meta__ import PROJECT_NAME
from .common import GithubHandler


PYPI_URL = f'https://pypi.org/pypi/{PROJECT_NAME}/json'


class ReleaseInfo(GithubHandler):
    def print(self, github: bool = True, pypi: bool = False) -> None:
        if github:
            self._print_github()
        if pypi:
            self._print_pypi()
        
    def _print_github(self) -> None:
        release: GitRelease
        if self.tag is None:
            release = self.repository.get_latest_release()
        
        else:
            try:
                release = next(r for r in self.repository.get_releases() if r.tag_name == self.tag)
            except StopIteration:
                print(f'release not found on github: {self.tag}')
                return

        print(f"""
        Release:    {release.title}
        Url:        {release.url}
        Created:    {release.created_at}
        Published:  {release.published_at}
        Draft:      {release.draft}
        Prerelease: {release.prerelease}
        Assets:     {', '.join(a.name for a in release.get_assets())}
        """)

    def _print_pypi(self) -> None:
        http: PoolManager = PoolManager()
        response: HTTPResponse = http.request('GET', PYPI_URL)
        if response.status != 200:
            print(f'error on pypi request: {response._request_url} ({response.status})')
            return

        project_data = json.loads(response.data)
        release_url: str = project_data['info']['release_url']
        downloads: Dict[str, int] = project_data['info']['downloads']

        version: str
        if self.tag is None:
            version = project_data['info']['version']
        else:
            version = self.tag[1:]
            release_url = release_url.replace(project_data['info']['version'], version)

        try:
            assets: List[Dict[str, str]] = project_data['releases'][version]
        except KeyError:
            print(f'release not found on pypi: {self.tag}')
            return

        uploaded: str
        if not any(assets):
            uploaded = 'no assets!'
        else:
            uploaded = assets[0]['upload_time'].replace('T', ' ')

        print(f"""
        Release:    {version}
        Url:        {release_url}
        Assets:     {', '.join(a['filename'] for a in assets)}
        Uploaded:   {uploaded}
        Downloads:
            Last Month: {downloads['last_month']}
            Last Week:  {downloads['last_week']}
            Last Day:   {downloads['last_day']}
        """)
