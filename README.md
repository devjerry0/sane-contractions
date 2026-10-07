# sane-contractions

[![Tests](https://github.com/devjerry0/sane-contractions/actions/workflows/commit.yml/badge.svg)](https://github.com/devjerry0/sane-contractions/actions/workflows/commit.yml)
[![codecov](https://codecov.io/gh/devjerry0/sane-contractions/branch/main/graph/badge.svg)](https://codecov.io/gh/devjerry0/sane-contractions)
[![PyPI](https://img.shields.io/pypi/v/sane-contractions.svg)](https://pypi.org/project/sane-contractions/)
[![Python versions](https://img.shields.io/pypi/pyversions/sane-contractions.svg)](https://pypi.org/project/sane-contractions/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/devjerry0/sane-contractions/blob/main/LICENSE)

Expand English contractions and slang in Python.

```python
import contractions

contractions.expand("I'm sure you'll love it!")
# 'I am sure you will love it!'
```

sane-contractions is a maintained fork of Pascal van Kooten's [contractions](https://github.com/kootenpv/contractions), which hasn't had a release since November 2022. The import name is still `contractions`, the word lists are the same, and the output matches the original's. The few API differences are listed under "Coming from contractions" below.

## Installation

```bash
pip install sane-contractions
```

Requires Python 3.10 or newer. If you have the original `contractions` package installed, uninstall it first. Both packages install a module named `contractions`, so only one of them can be present.

## Usage

`expand()` replaces every contraction it recognizes. Matching ignores case, and the replacement keeps the case of the original:

```python
contractions.expand("you're happy")   # 'you are happy'
contractions.expand("You're happy")   # 'You are happy'
contractions.expand("YOU'RE HAPPY")   # 'YOU ARE HAPPY'
```

Curly apostrophes, the kind Word and phone keyboards insert, work the same as straight ones:

```python
contractions.expand("you’re happy now")   # 'you are happy now'
```

A contraction always expands the same way. Nothing looks at the surrounding grammar, so ambiguous forms get their most common reading:

```python
contractions.expand("he's gone")     # 'he is gone', not 'he has gone'
contractions.expand("I'd done it")   # 'I would done it', not 'I had done it'
```

### Slang and leftovers

`expand()` has two flags, both on by default.

`slang` covers chat shorthand such as `idk`, `tbh` and `ppl`, plus contractions typed without the apostrophe:

```python
contractions.expand("dont worry, youre fine")
# 'do not worry, you are fine'
contractions.expand("dont worry, youre fine", slang=False)
# 'dont worry, youre fine'
```

Apostrophe-free spellings that are also ordinary words, like `its`, `well` and `ill`, are left alone. Some slang terms are ordinary words in technical writing, though, so turn `slang` off for that kind of text:

```python
contractions.expand("run git diff")               # 'run git different'
contractions.expand("run git diff", slang=False)  # 'run git diff'
```

`leftovers` covers dropped-g words like `goin'` and `nothin'`, and stray fragments such as `'ll` and `'re` that show up in tokenized text:

```python
contractions.expand("we were goin' home")                   # 'we were going home'
contractions.expand("we were goin' home", leftovers=False)  # "we were goin' home"
```

### Custom entries

```python
contractions.add("brb", "be right back")
contractions.add_dict({"afk": "away from keyboard", "lgtm": "looks good to me"})

contractions.expand("brb, lgtm")
# 'be right back, looks good to me'
```

To keep custom entries in files, store them as a JSON object that maps each contraction to its expansion:

```python
contractions.load_file("team_slang.json")   # {"lgtm": "looks good to me", ...}
contractions.load_folder("slang/")          # every *.json file in the folder
```

`load_folder()` doesn't look in subfolders. It reads files in name order, so if two files define the same key, the later file wins.

Custom entries are global. They apply to every later call in the process, whatever the flags, and they aren't saved anywhere. The matchers they're added to have no locking, so add your entries at startup, before other threads start calling `expand()`.

### Previewing

`preview()` lists matches without changing anything. It checks against every list, slang and leftovers included. `context_chars` sets how much text to show on each side of a match:

```python
contractions.preview("I'd love to see what you're thinking", context_chars=10)
# [{'match': "I'd", 'start': 0, 'end': 3, 'viewing_window': "I'd love to s"},
#  {'match': "you're", 'start': 21, 'end': 27, 'viewing_window': " see what you're thinking"}]
```

`e()` and `p()` are short aliases for `expand()` and `preview()`.

## API

| Function | Notes |
| --- | --- |
| `expand(text, leftovers=True, slang=True)` | Returns the expanded string. Raises `TypeError` if `text` isn't a `str`. |
| `preview(text, context_chars)` | Returns a list of dicts with `match`, `start`, `end` and `viewing_window`. |
| `add(contraction, expansion)` | Raises `TypeError` for non-strings and `ValueError` for empty strings. |
| `add_dict(mapping)` | Takes a `dict[str, str]`. Raises `TypeError` for anything that isn't a dict. |
| `load_file(path)` | Raises `FileNotFoundError`, `json.JSONDecodeError`, or `ValueError` if the file isn't a JSON object. |
| `load_folder(path)` | Raises `FileNotFoundError`, `NotADirectoryError`, or `ValueError` if the folder has no `.json` files. |
| `e`, `p` | Aliases for `expand` and `preview`. |
| `fix(text, leftovers=True, slang=True)` | Deprecated alias for `expand`. Emits a `DeprecationWarning` and will be removed in 1.0. |

## Coming from contractions

```bash
pip uninstall contractions
pip install sane-contractions
```

Positional calls to `fix()`, `add()` and `preview()` keep working. The differences:

- `fix()` emits a `DeprecationWarning`. Switch to `expand()` before 1.0.
- Some parameters were renamed: `preview(text, flank)` is now `preview(text, context_chars)`, and `add(key, value)` is now `add(contraction, expansion)`. This only matters if you pass them by keyword.
- The module no longer exposes its internals, such as `contractions.contractions_dict`, `contractions.slang_dict` and the `ts_*` matchers.

New in this fork: `add_dict()`, `load_file()`, `load_folder()`, the `e()` and `p()` aliases, and type hints that mypy and pyright pick up. The matchers are built on the first call rather than at import time, so `import contractions` does no setup work.

## Performance

Matching uses an Aho-Corasick automaton from [textsearch](https://github.com/kootenpv/textsearch), so each call scans the text once no matter how many entries are loaded. On an Apple M5 Max with Python 3.14, `expand()` handles a short sentence in about 3 µs (roughly 375,000 calls a second) and a 40 KB document in about 1.5 ms. To run the benchmarks on your own machine:

```bash
python tests/test_performance.py
```

## Contributing

Bug reports, new slang and pull requests are welcome. [CONTRIBUTING.md](https://github.com/devjerry0/sane-contractions/blob/main/CONTRIBUTING.md) covers setup, tests and conventions, and the [changelog](https://github.com/devjerry0/sane-contractions/blob/main/CHANGELOG.md) lists what changed in each release. Please report security issues privately, as described in [SECURITY.md](https://github.com/devjerry0/sane-contractions/blob/main/SECURITY.md).

## License

MIT. See [LICENSE](https://github.com/devjerry0/sane-contractions/blob/main/LICENSE).

The word lists and the original design come from Pascal van Kooten's [contractions](https://github.com/kootenpv/contractions) and its contributors.
