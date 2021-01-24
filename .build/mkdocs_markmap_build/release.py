import sys
from pprint import pprint
from typing import Dict, List
from github.Commit import Commit
from github.GitAuthor import GitAuthor
from github.GitCommit import GitCommit

from github.GitRelease import GitRelease
from github.GitReleaseAsset import GitReleaseAsset
from github.InputGitAuthor import InputGitAuthor

from .common import AssetCollector, ChangelogLoader, GithubHandler


MASTER_BRANCH = 'master'


class ReleaseHandler(GithubHandler):
    def __init__(self, tag: str) -> None:
        super(ReleaseHandler, self).__init__(tag)
        self._changelog = ChangelogLoader()
        self._collector = AssetCollector()

    def create(self, commit: str = None, dry_run: bool = True):
        release_message: str = self._changelog.get(self.tag)
        assets: List[str] = self._collector.get_assets()
        tagger: GitAuthor = None

        if commit is None:
            git_commit: GitCommit = self.repository.get_branch(MASTER_BRANCH).commit.commit
            commit = git_commit.sha
            tagger = git_commit.author
        
        else:
            git_commit: GitCommit = self.repository.get_commit(commit)
            tagger = git_commit.author

        parameters: Dict[str, str] = {
            'object': commit,
            'release_name': self.tag,
            'release_message': release_message,
            'tag': self.tag,
            'tag_message': f'Release version {self.tag}',
            'type': 'commit',
            'tagger': InputGitAuthor(tagger.name, tagger.email),
        }

        try:
            assert self.tag not in (tag.name for tag in self.repository.get_tags()), \
                f'tag "{self.tag}" already exists'
            assert self.tag not in (release.tag_name for release in self.repository.get_releases()), \
                f'release "{self.tag}" already exists'

        except AssertionError as e:
            print(e)
            sys.exit(1)

        if dry_run:
            print('This is a dry run!')
            pprint(parameters, width=120)
        
        else:
            release: GitRelease = self.repository.create_git_tag_and_release(**parameters, draft=True)
            print(f'Release "{self.tag}" created: {release.html_url}')
            for asset in assets:
                release_asset: GitReleaseAsset = release.upload_asset(asset)
                print(f'Release asset "{release_asset.name}" uploaded: {release_asset.url}')
            
            release.update_release(
                name=self.tag,
                message=release_message,
                draft=True,
            )
            print('Release published')

    def delete(self):
        try:
            next(t for t in self.repository.get_tags() if t.name == self.tag)

        except StopIteration:
            print(f'Tag "{self.tag}" does not exist')

        else:
            self.repository.get_git_ref(f'tags/{self.tag}').delete()
            print(f'Tag "{self.tag}" deleted')

        try:
            release: GitRelease = next(r for r in self.repository.get_releases() if r.tag_name == self.tag)

        except StopIteration:
            print(f'Release "{self.tag}" does not exist')

        else:
            release.delete_release()
            print(f'Release "{self.tag}" deleted')
