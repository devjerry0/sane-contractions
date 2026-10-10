# Changelog

Notable changes to this project are listed here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project uses [semantic versioning](https://semver.org/).

## [Unreleased]

### Fixed

- Contractions written with a curly apostrophe (`you’re`, `can’t`) are expanded again. A refactor before 0.2.0 broke the normalization step, so every release of this fork only matched straight apostrophes. Output now matches `contractions` 0.1.73.

### Added

- A `py.typed` marker, so mypy and pyright use the package's type hints.
- `SECURITY.md`, `CONTRIBUTING.md`, and issue and pull request templates.

### Changed

- Rewrote the README.
- Building from source requires setuptools 77 or newer.

## [0.3.2] - 2025-12-15

### Added

- `load_folder()`, which loads every `*.json` file in a directory.

### Fixed

- Tags created by the auto-tag workflow now trigger the PyPI publish workflow. 0.3.0 and 0.3.1 were tagged but never published.

## [0.3.1] - 2025-12-15

Tagged but not published to PyPI.

### Changed

- Internal cleanup: `pathlib` for file handling, complete type annotations, and stricter lint and type checks. No behavior changes.

## [0.3.0] - 2025-12-12

Tagged but not published to PyPI.

### Added

- `expand()`, which replaces `fix()`. `fix()` still works but emits a `DeprecationWarning`.
- `e()` and `p()` as short aliases for `expand()` and `preview()`.
- Type hints throughout.
- Argument checks that raise `TypeError` or `ValueError` with a clear message.

### Changed

- `load_json()` was renamed to `load_file()`.
- `preview()`'s `flank` parameter was renamed to `context_chars`.
- The matchers are built on the first call instead of at import time.

## [0.2.0] - 2025-12-12

First release as sane-contractions, forked from `contractions` 0.1.73.

### Added

- `add_dict()` and `load_json()` for adding many entries at once.

### Changed

- Requires Python 3.10 or newer.

[Unreleased]: https://github.com/devjerry0/sane-contractions/compare/v0.3.2...HEAD
[0.3.2]: https://github.com/devjerry0/sane-contractions/compare/v0.3.1...v0.3.2
[0.3.1]: https://github.com/devjerry0/sane-contractions/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/devjerry0/sane-contractions/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/devjerry0/sane-contractions/releases/tag/v0.2.0
