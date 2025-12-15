# sane-contractions

[![Tests](https://github.com/devjerry0/sane-contractions/actions/workflows/commit.yml/badge.svg)](https://github.com/devjerry0/sane-contractions/actions/workflows/commit.yml)
[![codecov](https://codecov.io/gh/devjerry0/sane-contractions/branch/main/graph/badge.svg)](https://codecov.io/gh/devjerry0/sane-contractions)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A fast and comprehensive Python library for expanding English contractions.

## Features

- ⚡ **Fast**: ~112K ops/sec for typical text expansion (Aho-Corasick algorithm)
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

[uv](https://github.com/astral-sh/uv)

## Quick Start

```python
import contractions

contractions.expand("you're happy now")
# "you are happy now"

contractions.expand("I'm sure you'll love it!")
# "I am sure you will love it!"

# Shorthand aliases
contractions.e("you're")  # "you are"
contractions.p("you're", 5)  # preview with context
```

## Usage

### Basic Contraction Expansion

```python
import contractions

text = "I'm sure you're going to love what we've done"
expanded = contractions.expand(text)
print(expanded)
# "I am sure you are going to love what we have done"
```

### Controlling Slang Expansion

```python
contractions.expand("yall're gonna love this", slang=True)
# "you all are going to love this"

contractions.expand("yall're gonna love this", slang=False)
# "yall are going to love this"

contractions.expand("yall're gonna love this", leftovers=False)
# "yall are gonna love this"
```

### Case Preservation

The library intelligently preserves the case pattern of the original contraction:

```python
contractions.expand("you're happy")    # "you are happy"
contractions.expand("You're happy")    # "You are happy"
contractions.expand("YOU'RE HAPPY")    # "YOU ARE HAPPY"
```

### Adding Custom Contractions

Add a single contraction:

```python
contractions.add('myword', 'my word')
contractions.expand('myword is great')
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

contractions.expand("ain't gonna happen")
# "are not going to happen"
```

Load contractions from a JSON file:

```python
# custom_contractions.json contains: {"myterm": "my expansion", "another": "another word"}
contractions.load_file("custom_contractions.json")

contractions.expand("myterm is great")
# "my expansion is great"
```

Load all JSON files from a folder:

```python
# Load all *.json files from a directory (ignores non-JSON files)
contractions.load_folder("./my_contractions/")

contractions.expand("myterm is great")
# "my expansion is great"
```

### Preview Contractions Before Fixing

The `preview()` function lets you see all contractions in a text before expanding them:

```python
text = "I'd love to see what you're thinking"
preview = contractions.preview(text, context_chars=10)

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

### `expand(text, leftovers=True, slang=True)`

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

### `load_file(filepath)`

Loads custom contractions from a JSON file.

**Parameters:**
- `filepath` (str): Path to JSON file containing contraction mappings

**Raises:**
- `FileNotFoundError`: If the file doesn't exist
- `json.JSONDecodeError`: If the file contains invalid JSON

### `load_folder(folderpath)`

Loads custom contractions from all JSON files in a directory. Non-JSON files are automatically ignored.

**Parameters:**
- `folderpath` (str): Path to directory containing JSON files

**Raises:**
- `FileNotFoundError`: If the folder doesn't exist
- `NotADirectoryError`: If the path is a file, not a directory
- `ValueError`: If no JSON files are found in the folder

### `preview(text, context_chars)`

Preview contractions in text before expanding.

**Parameters:**
- `text` (str): The text to analyze
- `context_chars` (int): Number of characters to show before/after each match

**Returns:** `list[dict]` - List of matches with context information

### `e(text, leftovers=True, slang=True)`

Shorthand alias for `expand()`.

### `p(text, context_chars)`

Shorthand alias for `preview()`.

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

- **~112K ops/sec** for typical text expansion (short texts with contractions)
- **~251K ops/sec** for preview operations (contraction detection)
- **~17K ops/sec** for medium texts with no contractions  
- **~13K ops/sec** for slang-heavy texts
- **~278K ops/sec** for adding custom contractions

Benchmarked on Apple M3 Max, Python 3.13.

Run performance benchmarks yourself:

```bash
# Create virtual environment and install
uv venv && source .venv/bin/activate
uv pip install -e .

# Run benchmarks
python tests/test_performance.py
```

## Requirements

- Python 3.10 or higher
- textsearch >= 0.0.21

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

```bash
git clone https://github.com/devjerry0/sane-contractions
cd sane-contractions
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"
```

### Running Tests

```bash
pytest tests/ --cov=contractions --cov-report=term-missing
```

### Code Quality

```bash
ruff check .
mypy contractions/ tests/
```

## What's Different from the Original?

This fork includes several enhancements over the original `contractions` library:

### 🆕 New Features
- **`add_dict()`** - Bulk add custom contractions from a dictionary
- **`load_file()`** - Load contractions from JSON files
- **`load_folder()`** - Load all JSON files from a directory
- **Type hints** - Full type coverage with mypy validation
- **Better structure** - Modular code organization with single-responsibility modules
- **Facade API** - Clean, simple public API with shorthand aliases (`e()`, `p()`)

### 🚀 Performance Improvements
- Lazy-loaded TextSearch instances (30x faster imports)
- Optimized dictionary operations and comprehensions
- Eliminated redundant code paths
- Reduced function call overhead

### 🧪 Testing
- **100% test coverage** enforced via CI/CD
- Comprehensive tests including edge cases
- Input validation and error handling tests
- Performance benchmarking suite

### 📦 Modern Tooling
- **Python 3.10+** support (modern type hints with `list[dict]`, etc.)
- Ruff for fast linting (replaces black, flake8, isort)
- Mypy for strict type checking
- GitHub Actions CI/CD with concurrency control
- Automated PyPI publishing via Git tags
- `uv` support for fast dependency management

### 📚 Better Documentation
- Comprehensive README with real benchmark results
- Complete API reference with examples
- Clear contributing guidelines

## Why "sane-contractions"?

**This is an enhanced fork of the original [contractions](https://github.com/kootenpv/contractions) library by Pascal van Kooten, with improvements in performance, testing, type safety, and maintainability.**

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
