import logging
import re
from functools import partial
from pathlib import Path
from typing import AnyStr, Dict, List, Optional

from markdown import Markdown
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor


log = logging.getLogger('mkdocs.markmap')


INCLUDE_SYNTAX = re.compile(r'\{!\s*(?P<path>.+?)\s*!\}')


class MarkmapPreprocessor(Preprocessor):
    """
    Wraps the content of the markdown with a code block for markmap.
    """

    def __init__(self, md: Markdown, config: Dict[str, str]):
        super(MarkmapPreprocessor, self).__init__(md)
        self.base_path: str = config['base_path']
        self.encoding: str = config['encoding']
        self.file_extension: str = config['file_extension']

    def run(self, lines: List[str]) -> List[str]:
        done: bool = False
        included_paths: List[Path] = []
        while not done:
            for loc, line in enumerate(lines):
                match: Optional[re.Match[AnyStr]] = INCLUDE_SYNTAX.search(line)
                if match is None:
                    continue

                path: Path = Path(match.group('path'))
                if not path.name.lower().endswith(self.file_extension):
                    continue

                if not path.is_absolute():
                    path = (Path(self.base_path) / path).resolve()

                if path in included_paths:
                    log.warning(f"loop detected while including: {path}")
                    continue

                included_paths.append(path)
                try:
                    with open(path, 'r', encoding=self.encoding) as r:
                        markmap: List[str] = r.readlines()
                        
                except Exception as e:
                    log.error('unable to include file {}. Ignoring statement. Error: {}'.format(path, e))
                    lines[loc] = INCLUDE_SYNTAX.sub('',line)
                    break

                line_split: List[str] = INCLUDE_SYNTAX.split(line)
                if len(markmap) == 0:
                    markmap.append('')
                else:
                    markmap.insert(0, '```markmap')
                    markmap.append('```')
                
                if line_split[0].strip() != '':
                    markmap.insert(0, line_split[0])

                if line_split[2].strip() != '':
                    markmap.append(line_split[2])

                lines = lines[:loc] + markmap + lines[loc+1:]
                break
                
            else:
                done = True

        return lines


class MarkmapExtension(Extension):
    config_defaults: Dict[str, str] = {
        'base_path': ['docs', 'Default location from which to evaluate relative paths for the include statement.'],
        'encoding': ['utf-8', 'Encoding of the files used by the include statement.'],
        'file_extension': ['.mm.md', 'File extension of mindmap files'],
    }

    def __init__(self, **configs: Dict[str, str]):
        self.config: Dict[str, str] = self.config_defaults
        for key, value in configs.items():
            self.setConfig(key, value)

    def extendMarkdown(self, md: Markdown, md_globals: Dict[str, str]) -> None:
        md.preprocessors.register(MarkmapPreprocessor(md, self.getConfigs()), 'include_markmap', 102)
        for extension in md.registeredExtensions:
            if extension.__class__.__name__ == 'SuperFencesCodeExtension':
                log.info(f'superfences detected by markmap')
                try:
                    from pymdownx.superfences import default_validator, fence_code_format, _formatter, _validator
                    extension.extend_super_fences(
                        'markmap',
                        partial(_formatter, class_name='language-markmap', _fmt=fence_code_format),
                        partial(_validator, validator=default_validator)
                    )
                    break

                except ImportError as e:
                    log.warning(f'markmap detected pymdownx.superfences, but import is not working: {e}')

                except Exception as e:
                    log.error(f'unexpected error: {e}')
