"""Check release metadata and the exact grammar pinned in the Zed manifest."""
import json
from pathlib import Path
import re
import subprocess
import tomllib

ROOT = Path(__file__).resolve().parents[1]
manifest = tomllib.loads((ROOT / 'extension.toml').read_text())
package = json.loads((ROOT / 'package.json').read_text())
lock = json.loads((ROOT / 'package-lock.json').read_text())
metadata = json.loads((ROOT / 'tree-sitter.json').read_text())['metadata']

def require(condition, message):
    if not condition:
        raise SystemExit(message)

version = manifest['version']
require(re.fullmatch(r'\d+\.\d+\.\d+', version), 'Use a stable X.Y.Z release version.')
require(all(value == version for value in (
    package['version'], lock['version'], lock['packages']['']['version'], metadata['version'],
)), 'Version mismatch between extension, package, lockfile and grammar metadata.')
require(re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', manifest['id']), 'Use a kebab-case extension ID.')
require(manifest['schema_version'] == 1, 'Unsupported extension schema.')
require(bool(manifest['authors']) and bool(manifest['description']), 'Missing extension metadata.')
require('Permission is hereby granted, free of charge' in (ROOT / 'LICENSE').read_text(),
        'The MIT license must remain available at the extension root.')
grammar = manifest['grammars']['mikrotik']
require(grammar['repository'] == manifest['repository'] == metadata['links']['repository'],
        'The grammar, extension and metadata repository URLs must match.')
require(grammar['repository'].startswith('https://github.com/'), 'Use an HTTPS GitHub repository.')
revision = grammar['rev']
require(re.fullmatch(r'[0-9a-f]{40}', revision), 'Pin the grammar to a complete commit SHA, not a branch.')
for relative in ('grammar.js', 'src/parser.c', 'src/grammar.json', 'src/node-types.json',
                 'src/tree_sitter/parser.h', 'src/tree_sitter/alloc.h', 'src/tree_sitter/array.h'):
    result = subprocess.run(['git', '-C', str(ROOT), 'show', f'{revision}:{relative}'], capture_output=True)
    require(result.returncode == 0, f'Cannot read {relative} at the pinned SHA; fetch repository history first.')
    require(result.stdout == (ROOT / relative).read_bytes(),
            f'{relative} differs from the pinned grammar; publish its commit and update the SHA before release.')
print(f'PASS: release {version}, MIT license, synchronized versions and grammar pinned to {revision}.')
print('Manual Zed validation and registry submission remain separate steps; see PUBLISHING.md.')
