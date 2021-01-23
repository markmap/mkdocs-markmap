import os
import sys
from typing import List

from twine.cli import dispatch

from mkdocs_markmap.__meta__ import PROJECT_NAME
from .common import AssetDownloader, GithubHandler


class DistributionHandler(object):
    def __init__(self, tag: str) -> None:
        self._collector = AssetDownloader(tag)

    def distribute(self):
        assets: List[str] = self._collector.get_assets_from_release()
        os.environ['TWINE_USERNAME'] = '__token__'

        dispatch(['check', *assets])

        if os.environ.get('TWINE_PASSWORD') is None:
            print('environment variable "TWINE_PASSWORD" is not set')
            sys.exit(1)

        dispatch(['upload', *assets])
