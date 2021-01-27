import sys
from distutils.core import run_setup
from pathlib import Path

from invoke import task

PROJECT_PATH: Path = Path(__file__).parent.absolute()
sys.path.insert(0, str(PROJECT_PATH / '.build'))

from mkdocs_markmap.__meta__ import PROJECT_VERSION
from mkdocs_markmap_build.common import ChangelogLoader
from mkdocs_markmap_build.distribution import DistributionHandler
from mkdocs_markmap_build.release import ReleaseHandler


TARGET_TAG = f'v{PROJECT_VERSION}'


@task
def verify(c, tag=TARGET_TAG):
    print('verify integrity: {tag}')

    handler: ReleaseHandler = ReleaseHandler(tag)
    handler.verify()


@task
def build(c):
    run_setup('setup.py', script_args=['sdist', 'bdist_wheel'])


@task
def delete_release(c, tag=TARGET_TAG, yes=False):
    print(f'delete tag and release: {tag}')

    if not yes and input('Are you sure [y/N]? ').lower() != 'y':
        print('aborted by user')
        sys.exit(1)
    
    handler: ReleaseHandler = ReleaseHandler(tag)
    handler.delete()


@task
def release(c, commit=None, tag=TARGET_TAG, dry_run=True):
    print(f'create tag and release: {tag}')

    handler: ReleaseHandler = ReleaseHandler(tag)
    handler.create(commit, dry_run=dry_run)


@task
def distribute(c, tag=TARGET_TAG, dry_run=True):
    print(f'distribute release: {tag}')

    handler: DistributionHandler = DistributionHandler(tag)
    handler.distribute(dry_run=dry_run)
