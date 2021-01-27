# mkdocs-markmap

> Beautiful and simple mindmaps written in markdown.

[![MIT license](https://badgen.net/github/license/neatc0der/mkdocs-markmap)](https://github.com/neatc0der/mkdocs-markmap/blob/master/LICENSE)
[![PyPI](https://badgen.net/pypi/v/mkdocs-markmap)](https://pypi.org/project/mkdocs-markmap/)
[![Latest Release](https://badgen.net/github/release/neatc0der/mkdocs-markmap/latest)](https://github.com/neatc0der/mkdocs-markmap/releases/latest)
[![Open Issues](https://badgen.net/github/open-issues/neatc0der/mkdocs-markmap)](https://github.com/neatc0der/mkdocs-markmap/issues)
[![Open PRs](https://badgen.net/github/open-prs/neatc0der/mkdocs-markmap)](https://github.com/neatc0der/mkdocs-markmap/pulls)

This is a plugin and an extension for [mkdocs](https://github.com/mkdocs/mkdocs/) to add [markmap](https://github.com/gera2ld/markmap).

## Prerequisits

This plugin was tested with, but is not limited to:

* Python 3.8
* mkdocs 1.1

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

## Advanced Settings

There are more options available for `mkdocs.yml` (shown values are defaults):

```yaml
plugins:
  - markmap:
      base_path: docs
      encoding: utf-8
      file_extension: .mm.md
      d3_version: 6.3.1
      lib_version: 0.11.1
      view_version: 0.2.1
```

In addition, feel free to define your favourite source urls like this:

```yaml
extra_javascript:
  - https://unpkg.com/d3@6.3.1/dist/d3.min.js
  - https://unpkg.com/markmap-lib@0.11.1/dist/browser/index.min.js
  - https://unpkg.com/markmap-view@0.2.1/dist/index.min.js
```

:warning: The urls need to contain one of these keywords to be considered as deviation from default:

* `d3`
* `markmap-lib`
* `markmap-view`

## Credits :clap:

Some of the development approaches are based on implementations provided by the following projects:

* [markmap](https://github.com/gera2ld/markmap) (key feature of this project)
* [markdown-include](https://github.com/cmacmackin/markdown-include) (basis for extension support)
* [mkdocs-mermaid2-plugin](https://github.com/fralau/mkdocs-mermaid2-plugin) (basis for plugin support)
