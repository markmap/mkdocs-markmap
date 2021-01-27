from pathlib import Path
from setuptools import setup, find_packages
from typing import List

from mkdocs_markmap.__meta__ import PROJECT_NAME, PROJECT_VERSION, REPOSITORY_NAME


def readme() -> str:
    """print long description"""
    with open('README.md') as f:
        return f.read()


def get_requirements(filename: str, base_dir: str = 'requirements') -> List[str]:
    """Load list of dependencies."""
    install_requires = []
    with open(Path(base_dir) / filename) as fp:
        for line in fp:
            stripped_line = line.partition('#')[0].strip()
            if stripped_line:
                install_requires.append(stripped_line)

    return install_requires


setup(
    name=PROJECT_NAME,
    version=PROJECT_VERSION,
    description='MkDocs plugin and extension to creates mindmaps from markdown using markmap',
    long_description=readme(),
    long_description_content_type='text/markdown',
    keywords='mkdocs python markdown markmap mindmap include',
    url=f'https://github.com/{REPOSITORY_NAME}',
    author='neatc0der',
    author_email='',
    license='MIT',
    python_requires='>=3.6',
    install_requires=get_requirements('prod.txt'),
    setup_requirements=get_requirements('build.txt'),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    packages=find_packages(exclude=['*.tests']),
    package_dir={
        'mkdocs_markmap': 'mkdocs_markmap',
    },
    package_data={
        'mkdocs_markmap': ['static_files/*'],
    },
    entry_points={
        'mkdocs.plugins': [
            'markmap = mkdocs_markmap.plugin:MarkmapPlugin',
        ],
        'markdown.extensions': [
            'markmap = mkdocs_markmap.extension:MarkmapExtension',
        ]
    },
)
