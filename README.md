# mkdocs-markmap

> Beautiful and simple mindmaps written in markdown.

[![MIT license](https://badgen.net/github/license/markmap/mkdocs-markmap)](https://github.com/markmap/mkdocs-markmap/blob/master/LICENSE)
[![PyPI](https://badgen.net/pypi/v/mkdocs-markmap)](https://pypi.org/project/mkdocs-markmap/)
[![Latest Release](https://badgen.net/github/release/markmap/mkdocs-markmap/latest)](https://github.com/markmap/mkdocs-markmap/releases/latest)
[![Open Issues](https://badgen.net/github/open-issues/markmap/mkdocs-markmap)](https://github.com/markmap/mkdocs-markmap/issues)
[![Open PRs](https://badgen.net/github/open-prs/markmap/mkdocs-markmap)](https://github.com/markmap/mkdocs-markmap/pulls)

This is a plugin and an extension for [mkdocs](https://github.com/mkdocs/mkdocs/) to add [markmap](https://github.com/markmap/markmap).

## Prerequisits

This plugin was tested with, but is not limited to:

* Python 3.9
* mkdocs 1.3

## Quickstart

### Install

```bash
pip install mkdocs-markmap
```

### Configure

Add this to `mkdocs.yml`:

```yaml
plugins:
  - markmap
```

## Usage

This plugin supports code blocks of markdown as follows:

````markdown
```markmap
# Root

## Branch 1

* Branchlet 1a
* Branchlet 1b

## Branch 2

* Branchlet 2a
* Branchlet 2b
```
````

It can also make use of file includes to keep your markdown tidy:

```markdown
Look at this beautiful mindmap:

{!mindmap.mm.md!}
```

## Advanced Settings

There are more options available for `mkdocs.yml` (shown values are defaults):

```yaml
plugins:
  - markmap:
      base_path: docs
      encoding: utf-8
      file_extension: .mm.md
      d3_version: 7
      lib_version: 0.15.3
      view_version: 0.15.3
```

In addition, feel free to define your favourite source urls like this:

```yaml
plugins:
  - markmap:
      # disable the default assets first
      d3_version: ''
      lib_version: ''
      view_version: ''

extra_javascript:
  - https://unpkg.com/d3@7/dist/d3.min.js
  - https://unpkg.com/markmap-lib@0.15.3/dist/browser/index.js
  - https://unpkg.com/markmap-view@0.15.3/dist/browser/index.js
```

## Troubleshooting

### Nav tree lists markmaps

1. Move your markmap files to a separate folder next to `docs`, e.g. `mindmaps`
2. Configure `base_path` accordingly (see [Advanced Settings](#advanced-settings))

### Static javascript files not working

1. Ensure naming of javascript files matches the scheme (see [Advanced Settings](#advanced-settings))
2. Copy all javascript files to `doc/js/`, otherwise `mkdocs` will not copy static files to `site/`
3. Define all files in `extra_javascript`, e.g.

```yaml
extra_javascript:
  - js/markmap-d3.js
  - js/markmap-lib.js
  - js/markmap-view.js
```

### Usage of proxy is preventing download of javascript files

Usually proxies should be supported by `requests`, which is used for downloading all required javascript files. If the issue remains, try downloading the files yourself and store them accordingly (see [Static javascript files not working](#static-javascript-files-not-working))

## Credits :clap:

Some of the development approaches are based on implementations provided by the following projects:

* [markmap](https://github.com/markmap/markmap) (key feature of this project)
* [markdown-include](https://github.com/cmacmackin/markdown-include) (basis for extension support)
* [mkdocs-mermaid2-plugin](https://github.com/fralau/mkdocs-mermaid2-plugin) (basis for plugin support)
