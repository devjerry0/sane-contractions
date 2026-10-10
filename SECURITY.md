# Security Policy

sane-contractions is maintained by Jeremy Bruns ([@devjerry0](https://github.com/devjerry0)). Security reports come straight to me.

## Supported versions

Security fixes go into the latest release on PyPI. If you're on an older version, upgrade first and check whether the problem is still there.

## Reporting a vulnerability

Please don't open a public issue. Report it privately through GitHub instead:

https://github.com/devjerry0/sane-contractions/security/advisories/new

It helps to include:

- the sane-contractions and Python versions you're using
- the smallest input or JSON file that triggers the problem
- what happens, and what you expected to happen

I'll acknowledge your report within a week and keep you updated while I work on a fix. Once the fix is released, I'll publish a GitHub security advisory and credit you, unless you'd rather stay anonymous.

## Scope

sane-contractions works on strings in memory and reads the JSON files you pass to `load_file()` and `load_folder()`. It makes no network requests and never executes anything it loads. Things worth reporting include:

- input that makes `expand()` or `preview()` hang or use runaway amounts of memory
- a JSON file that makes `load_file()` or `load_folder()` do anything besides parse JSON
- a weakness in the release workflow that could let someone publish a tampered package to PyPI

Problems in `textsearch` or its dependencies belong with those projects, but I'd still like a heads-up if they affect this package.
