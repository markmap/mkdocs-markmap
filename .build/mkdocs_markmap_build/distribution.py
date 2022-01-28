import os
import sys
from typing import List
import requests

from twine.cli import dispatch

from mkdocs_markmap.__meta__ import PROJECT_NAME, REPOSITORY_URL
from .common import AssetDownloader


MASTODON_URL: str = "https://fosstodon.org"


class DistributionHandler(object):
    def __init__(self, tag: str) -> None:
        self._collector: AssetDownloader = AssetDownloader(tag)

    def distribute(self, dry_run: bool = True):
        assets: List[str] = self._collector.get_assets_from_release()
        os.environ['TWINE_USERNAME'] = '__token__'

        dispatch(['check', *assets])

        if os.environ.get('TWINE_PASSWORD') is None:
            print('environment variable "TWINE_PASSWORD" is not set')
            sys.exit(1)

        if dry_run:
            print('This is a dry run!')

        else:
            dispatch(['upload', *assets])


class MastodonHandler(object):
    def __init__(self, tag: str) -> None:
        self.tag = tag
        self._url: str = f"{REPOSITORY_URL}/releases/{tag}"

    def post(self):
        auth_token: str = os.environ.get('MASTODON_TOKEN')
        if auth_token is None:
            print('environment variable "MASTODON_TOKEN" is not set')
            sys.exit(1)

        response: requests.Response = requests.post(f"{MASTODON_URL}/api/v1/statuses", data={
            "status": f"🆕 {PROJECT_NAME} {self.tag}\n{self._url}",
        }, headers={"Authorization": f"Bearer {auth_token}"})
        if not response.ok:
            print(f"unable to post status on mastodon: {response.text} ({response.status_code})")
