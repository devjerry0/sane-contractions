# Contributing

Thanks for helping out. Bug reports, new contractions and slang, and code changes are all welcome.

## Reporting bugs

Open an issue with:

- the version (`python -c "import contractions; print(contractions.__version__)"`)
- the input text and the flags you passed
- what you got and what you expected

For anything security-related, follow [SECURITY.md](SECURITY.md) instead of opening an issue.

## Adding or changing entries

The word lists live in `contractions/data/`:

| File | Used |
| --- | --- |
| `contractions_dict.json` | always |
| `leftovers_dict.json` | when `leftovers=True` |
| `slang_dict.json` | when `slang=True` |
| `safety_keys.json` | lists contractions like `we'll` whose apostrophe-free spelling (`well`) is a real word, so slang mode never generates it |

Keys are lowercase. Matching is case-insensitive, and the case of the input is carried over to the output. Add a test in `tests/test_contractions.py` for anything you add or change.

## Development setup

You'll need Python 3.10 or newer and [uv](https://github.com/astral-sh/uv) (plain `pip` works too).

```bash
git clone https://github.com/devjerry0/sane-contractions
cd sane-contractions
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"
```

## Checks

CI runs these on every pull request to `main`, with tests on Python 3.10 through 3.14. Please run them before asking for a review:

```bash
ruff check .
mypy contractions/ tests/
pytest --cov=contractions
```

Coverage is held at 100%, so new code needs tests. Bug fixes should start with a test that fails without the fix.

## Pull requests

- Branch from `main` and keep each pull request to one change.
- Write commit messages in the [Conventional Commits](https://www.conventionalcommits.org/) style used in the history (`fix: ...`, `feat: ...`, `docs: ...`).
- Add a line under "Unreleased" in [CHANGELOG.md](CHANGELOG.md) for anything users would notice.

## Releases

This part is for maintainers. Move the "Unreleased" changelog entries under a new version heading, bump `__version__` in `contractions/_version.py`, and merge to `main`. The `auto-tag` workflow tags the commit, and the tag triggers the `publish` workflow, which runs the checks and uploads to PyPI.
