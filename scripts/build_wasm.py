"""Compile the grammar with the same flags used by the Zed extension builder."""
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
sdk = os.environ.get('WASI_SDK_PATH')
if not sdk:
    raise SystemExit('Set WASI_SDK_PATH to a wasi-sdk installation; see PUBLISHING.md.')
clang = Path(sdk) / 'bin' / ('clang.exe' if os.name == 'nt' else 'clang')
if not clang.is_file():
    raise SystemExit(f'WASI SDK clang not found: {clang}')
output = ROOT / 'build' / 'grammars' / 'mikrotik.wasm'
output.parent.mkdir(parents=True, exist_ok=True)
subprocess.run([
    str(clang), '-fPIC', '-shared', '-Os', '-Wl,--export=tree_sitter_mikrotik',
    '-o', str(output), '-I', str(ROOT / 'src'), str(ROOT / 'src/parser.c'),
], check=True)
# Parse the complete WASM module, not just its magic bytes or file size.
subprocess.run([
    'node', '--input-type=module', '-e',
    'import fs from "node:fs"; '
    'const module = new WebAssembly.Module(fs.readFileSync(process.argv[1])); '
    'if (!WebAssembly.Module.exports(module).some(e => e.name === "tree_sitter_mikrotik" && e.kind === "function")) '
    '{ throw new Error("Missing grammar export"); }',
    str(output),
], check=True)
print(f'PASS: WASM module compiled and validated with tree_sitter_mikrotik export: {output}')
