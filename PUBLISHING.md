# Publishing 0.1.0

Target: the [Zed extension registry](https://github.com/zed-industries/extensions).
This repository is the extension source, not an npm package. Keep `private: true`
in `package.json`; do not use `npm publish`.

## Automated validation

```sh
npm ci
npm run check
npm run check:release
```

CI additionally regenerates the parser and checks for drift, audits dependencies,
and builds a WebAssembly grammar using WASI SDK 34. The SDK archive is verified
against its published GitHub asset SHA-256 before extraction.

To compile locally, install an official [wasi-sdk](https://github.com/WebAssembly/wasi-sdk/releases),
verify its archive against the release digest, set `WASI_SDK_PATH` to its extracted
directory, then run:

```sh
npm run build:wasm
```

This validates compilation and the grammar export; it does not replace running
the extension in Zed. Generated `build/` files are not committed.

## Before submitting

- [ ] Merge the preparation PR and check that CI passes on the resulting commit.
- [ ] Run `npm run check:release` on that commit. The grammar SHA must remain
      reachable on the public repository and match the grammar/parser files.
- [ ] In Zed, use **Install Dev Extension** and select the repository root at the
      exact commit intended for submission. This uses the published, pinned
      grammar, rather than the development helper's local snapshot.
- [ ] Open `examples/router.rsc`. Confirm `.rsc` detection, comments, strings
      containing `#`, interpolation, network literals, bracket matching and
      indentation. Record the Zed version, OS and commit in the registry PR.
- [ ] Confirm the ID `mikrotik` is still unused and there is no equivalent
      RouterOS extension in the registry. Both were absent when preparing this PR.
- [ ] Replace `Unreleased` in `CHANGELOG.md` with the release date once approved.
      If this changes the submitted commit, repeat the manual Zed check there.

Manual testing at the submitted commit is a Zed publishing requirement. It is
still pending; the cloud environment has no Zed UI.

## Submit to the registry

After the checklist is complete, fork and clone `zed-industries/extensions`,
create a submission branch, and add this repository as an HTTPS submodule:

```sh
git submodule add https://github.com/BatistaFelipe/MikrotikScript extensions/mikrotik
git -C extensions/mikrotik checkout <tested-release-commit>
```

The tested commit must be present on a public branch. Add this entry to the
registry's top-level `extensions.toml`:

```toml
[mikrotik]
submodule = "extensions/mikrotik"
version = "0.1.0"
```

Run `pnpm sort-extensions` in the registry checkout, commit using Conventional
Commits, push your fork and open a PR to `zed-industries/extensions`. Submit only
this extension. Registry maintainers review and publish it after merging.

GitHub tags/releases are optional and do not publish to the Zed registry. This
preparation does not create tags, GitHub releases or a registry submission.

## Future updates

For grammar changes, first merge/push the grammar commit, then update
`grammars.mikrotik.rev` to that full SHA. Keep release versions synchronized in
`extension.toml`, `package.json`, `package-lock.json` and `tree-sitter.json`.
Rerun the checks and manual Zed test, then update the registry submodule and
version entry. Query-only changes do not require a new grammar SHA.

References: [prerequisites](https://zed.dev/docs/extensions/publishing/prerequisites),
[licenses](https://zed.dev/docs/extensions/publishing/license-requirements),
[submission guide](https://zed.dev/docs/extensions/publishing/publishing-guide).
