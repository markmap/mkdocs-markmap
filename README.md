# mkdocs-markmap

This is a plugin and an extension for [mkdocs](https://github.com/mkdocs/mkdocs/) to add [markmap](https://github.com/gera2ld/markmap).

## Prerequisits

This plugin was tested with, but is not limited to:

* Python 3.8
* mkdocs 1.1

## How to integrate this?

### Install

```bash
pip install mkdocs-markmap
```

### Configure

Add this to `mkdocs.yml`:

```yaml
markdown_extensions:
  - markmap:
      base_path: docs
      encoding: utf-8
      file_extension: .mm.md
plugins:
  - markmap:
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

:warning: The urls needs contain one of these keywords to be considered as deviation from default:

* `d3`
* `markmap-lib`
* `markmap-view`

## Wait, what?! Do I need an extension or a plugin? :unamused:

_Q: What does the plugin do?_

A: It supports code blocks of markdown as follows:

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

_Q: What does the extension do?_

A: Well, having such a support is nice, but huge mindmap blocks might be annoying within your tidy markdown files. That is why the extension provides an addition to the markdown syntax. It includes files whereever you need them to be:

```markdown
Look at this beautiful mindmap:

{!mindmap.mm.md!}
```

But you _do_ need the plugin for that. Thus, don't forget to follow the setup example above.

## Credits :clap:

Some of the development approaches are based on implementations provided by the following projects:

* [markmap](https://github.com/gera2ld/markmap) (key feature of this project)
* [markdown-include](https://github.com/cmacmackin/markdown-include) (basis for extension support)
* [mkdocs-mermaid2-plugin](https://github.com/fralau/mkdocs-mermaid2-plugin) (basis for plugin support)
