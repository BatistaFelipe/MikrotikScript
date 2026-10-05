# MikroTik RouterOS for Zed

Syntax highlighting for MikroTik RouterOS configuration and scripts (`.rsc`) in
Zed. Includes bracket matching and indentation, using Tree-sitter without a
language server or custom Rust code.

## Install and test locally

This extension has not yet been submitted to the Zed registry. In Zed, open
**Extensions > Install Dev Extension**, select this repository's root directory,
then open `examples/router.rsc`. The manifest uses a fixed public grammar commit.
Zed automatically downloads the WASI SDK needed to compile it. Follow the dev
extension prerequisites for your Zed version.

## Develop

Requirements: Node.js/npm, Python 3.11+, Git and a C compiler for native tests.
The Tree-sitter CLI version is pinned in the lockfile.

```sh
npm ci
npm run generate
npm run check
npm run prepare:zed
```

`npm run check` runs the corpus tests, checks a representative export and validates
the Zed queries. `npm test` runs only the corpus suite.

When editing the grammar, `npm run prepare:zed` creates an isolated local grammar
commit and extension snapshot under `.zed-dev/`, without committing to or pushing
this project. Select the printed `extension` directory in **Install Dev Extension**.
Regenerate the parser and prepare/reinstall a new snapshot after changes. Keep
snapshots needed by an installed dev extension until it has been replaced.

If the default cache directories are read-only, use writable ones:

```sh
export npm_config_cache=/tmp/mikrotik-npm-cache
export XDG_CACHE_HOME=/tmp/mikrotik-tree-sitter-cache
```

## Coverage and limitations

- Comments, line continuation, strings, escapes and interpolation.
- Variables, quoted variable names, control words and colon-prefixed commands.
- Menu paths, common commands, properties followed by `=` and operators.
- IPv4/CIDR, IPv6, MAC addresses, numbers and durations.
- Nested blocks, expressions and command substitutions.

This structural grammar does not validate RouterOS commands, properties or
address ranges. Coverage does not yet include every date format, IPv6 zone or
embedded IPv4 form, or every escape combination in interpolated expressions.
See `test/corpus/` and `scripts/check.py` for verified behavior. Visual appearance
depends on the Zed theme and requires testing in the editor.

## Release preparation

Version: **0.1.0**, not yet published. See [PUBLISHING.md](PUBLISHING.md) for the
release checks, required manual testing and registry submission steps, and
[CHANGELOG.md](CHANGELOG.md) for release notes. The MIT license is in [LICENSE](LICENSE).

## Review agents and commits

Agent definitions supplied for code and security reviews are in `.claude/agents/`.
They retain the Claude Code format and `model: sonnet` metadata. Invoke them by
name in Claude Code, or supply their guidance to your review tool using its
available model and tools. They are not required to install the Zed extension.

Use Conventional Commits, for example `feat(zed): add language support`,
`fix(parser): preserve string content` and `chore(ci): validate release metadata`.

References: [Zed language extensions](https://zed.dev/docs/extensions/languages),
[extension development](https://zed.dev/docs/extensions/developing-extensions).
