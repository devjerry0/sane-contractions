# sane-contractions

[![Tests](https://github.com/devjerry0/sane-contractions/actions/workflows/commit.yml/badge.svg)](https://github.com/devjerry0/sane-contractions/actions/workflows/commit.yml)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)](https://github.com/devjerry0/sane-contractions)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A fast and comprehensive Python library for expanding English contractions and slang.

**This is an enhanced fork of the original [contractions](https://github.com/kootenpv/contractions) library by Pascal van Kooten, with significant improvements in performance, testing, type safety, and maintainability.**

## Features

- ⚡ **Fast**: 50x faster than version 0.0.18 (uses efficient Aho-Corasick algorithm)
- 📚 **Comprehensive**: Handles standard contractions, slang, and custom additions
- 🎯 **Smart**: Preserves case and handles ambiguous contractions intelligently
- 🔧 **Flexible**: Easy to add custom contractions on the fly
- 🐍 **Modern**: Supports Python 3.10+

## Installation

### Using pip

```bash
pip install sane-contractions
```

### Using uv (Recommended - Much Faster!)

```bash
uv pip install sane-contractions
```

[uv](https://github.com/astral-sh/uv) is 10-100x faster than pip. See [UV_USAGE.md](UV_USAGE.md) for more details.

## Quick Start

```python
import contractions

contractions.fix("you're happy now")
# "you are happy now"

contractions.fix("I'm sure you'll love it!")
# "I am sure you will love it!"
```

## Usage

### Basic Contraction Expansion

```python
import contractions

text = "I'm sure you're going to love what we've done"
expanded = contractions.fix(text)
print(expanded)
# "I am sure you are going to love what we have done"
```

### Controlling Slang Expansion

```python
contractions.fix("yall're gonna love this", slang=True)
# "you all are going to love this"

contractions.fix("yall're gonna love this", slang=False)
# "yall are going to love this"

contractions.fix("yall're gonna love this", leftovers=False)
# "yall are gonna love this"
```

### Case Preservation

The library intelligently preserves the case pattern of the original contraction:

```python
contractions.fix("you're happy")    # "you are happy"
contractions.fix("You're happy")    # "You are happy"
contractions.fix("YOU'RE HAPPY")    # "YOU ARE HAPPY"
```

### Adding Custom Contractions

Add a single contraction:

```python
contractions.add('myword', 'my word')
contractions.fix('myword is great')
# "my word is great"
```

Add multiple contractions at once:

```python
custom_contractions = {
    "ain't": "are not",
    "gonna": "going to",
    "wanna": "want to",
    "customterm": "custom expansion"
}
contractions.add_dict(custom_contractions)

contractions.fix("ain't gonna happen")
# "are not going to happen"
```

Load contractions from a JSON file:

```python
# custom_contractions.json contains: {"myterm": "my expansion", "another": "another word"}
contractions.load_json("custom_contractions.json")

contractions.fix("myterm is great")
# "my expansion is great"
```

### Preview Contractions Before Fixing

The `preview()` function lets you see all contractions in a text before expanding them:

```python
text = "I'd love to see what you're thinking"
preview = contractions.preview(text, flank=10)

for item in preview:
    print(f"Found '{item['match']}' at position {item['start']}")
    print(f"Context: {item['viewing_window']}")

# Output:
# Found 'I'd' at position 0
# Context: I'd love to
# Found 'you're' at position 21  
# Context: what you're thinkin
```

## API Reference

### `fix(text, leftovers=True, slang=True)`

Expands contractions in the given text.

**Parameters:**
- `text` (str): The text to process
- `leftovers` (bool): Whether to expand leftover contractions (default: True)
- `slang` (bool): Whether to expand slang terms (default: True)

**Returns:** `str` - Text with contractions expanded

### `add(key, value)`

Adds a single custom contraction.

**Parameters:**
- `key` (str): The contraction to match
- `value` (str): The expansion

### `add_dict(dictionary)`

Adds multiple custom contractions at once.

**Parameters:**
- `dictionary` (dict): Dictionary mapping contractions to their expansions

### `load_json(filepath)`

Loads custom contractions from a JSON file.

**Parameters:**
- `filepath` (str): Path to JSON file containing contraction mappings

**Raises:**
- `FileNotFoundError`: If the file doesn't exist
- `json.JSONDecodeError`: If the file contains invalid JSON

### `preview(text, flank)`

Preview contractions in text before expanding.

**Parameters:**
- `text` (str): The text to analyze
- `flank` (int): Number of characters to show before/after each match

**Returns:** `list[dict]` - List of matches with context information

## Examples

### Standard Contractions

```python
you're  -> you are
I'm     -> I am
we'll   -> we will
it's    -> it is
they've -> they have
```

### Slang Terms

```python
gonna   -> going to
wanna   -> want to
gotta   -> got to
yall    -> you all
ain't   -> are not
```

### Month Abbreviations

```python
jan. -> january
feb. -> february
mar. -> march
```

### Ambiguous Cases

For ambiguous contractions, the library uses the most common expansion:

```python
he's -> he is  (not "he has")
```

## Performance

The library uses the Aho-Corasick algorithm for efficient string matching, achieving:

- **~256K ops/sec** for short texts
- **~17K ops/sec** for medium texts with no contractions  
- **~13K ops/sec** for slang-heavy texts

Run performance benchmarks:

```bash
# Make sure package is installed in development mode
pip install -e .

python tests/test_performance.py
```

## Requirements

- Python 3.10 or higher
- textsearch >= 0.0.21

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

```bash
git clone https://github.com/kootenpv/contractions
cd contractions
pip install -e .
pip install pytest pytest-cov ruff mypy
```

### Running Tests

```bash
# Run tests
pytest tests/ -v

# Run tests with coverage
pytest tests/ --cov=contractions --cov-report=term-missing
```

### Code Quality

```bash
ruff check .
mypy contractions/__init__.py tests/
```

## What's Different from the Original?

This fork includes several enhancements over the original `contractions` library:

### 🆕 New Features
- **`add_dict()`** - Bulk add custom contractions from a dictionary
- **`load_json()`** - Load contractions from JSON files
- **Type hints** - Full type coverage with mypy validation
- **Better structure** - Modular code organization (core, api modules)

### 🚀 Performance Improvements
- Optimized dictionary operations using `|=` operator
- Reduced function call overhead
- Improved list comprehensions
- Cached computations

### 🧪 Enhanced Testing
- **100% test coverage** (up from ~60%)
- 16 comprehensive tests including edge cases
- Error handling tests
- Performance benchmarking suite

### 📦 Modern Tooling
- **Python 3.10+** support (modern type hints)
- Ruff for fast linting
- Pre-commit hooks
- GitHub Actions CI/CD
- Automated PyPI publishing

### 📚 Better Documentation
- Comprehensive README with examples
- API reference documentation
- Deployment guide
- Contributing guidelines

## Why "sane-contractions"?

The original library is excellent but has been unmaintained since 2021. This fork provides:
- Active maintenance
- Modern Python practices
- Community contributions
- Regular updates

## License

MIT License - see LICENSE file for details.

## Credits

**Original Author:** Pascal van Kooten (@kootenpv)  
**Fork Maintainer:** Jeremy Bruns  
**Original Repository:** https://github.com/kootenpv/contractions

This project would not exist without Pascal's excellent foundation. All credit for the core concept and initial implementation goes to the original author.
