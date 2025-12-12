# Using sane-contractions with uv

[uv](https://github.com/astral-sh/uv) is a blazingly fast Python package installer and resolver written in Rust by Astral (creators of Ruff).

## Installation

### Install uv (if you haven't already)

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or with pip
pip install uv
```

### Install sane-contractions with uv

```bash
# Add to your project
uv pip install sane-contractions

# Or in a virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install sane-contractions
```

### Install for development

```bash
# Clone the repository
git clone https://github.com/devjerry0/sane-contractions.git
cd sane-contractions

# Create virtual environment with uv
uv venv

# Activate it
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in editable mode with dev dependencies
uv pip install -e ".[dev]"

# Run tests
pytest tests/ -v
```

## Why use uv?

- ⚡ **10-100x faster** than pip
- 🔒 **Better dependency resolution** 
- 🎯 **Drop-in replacement** for pip
- 🦀 **Written in Rust** for maximum performance
- 🛠️ **Modern tooling** from the Ruff team

## Usage Examples

### Install specific version

```bash
uv pip install sane-contractions==0.1.72
```

### Install with extras

```bash
# With dev dependencies
uv pip install sane-contractions[dev]
```

### Update package

```bash
uv pip install --upgrade sane-contractions
```

### Sync dependencies from requirements.txt

```bash
uv pip sync requirements.txt
```

## Performance Comparison

Traditional pip:
```bash
pip install sane-contractions  # ~2-5 seconds
```

With uv:
```bash
uv pip install sane-contractions  # ~0.1-0.5 seconds
```

## Integration with pyproject.toml

The package uses modern `pyproject.toml` with all metadata defined, making it fully compatible with uv's dependency resolution.

```toml
[project]
name = "sane-contractions"
dependencies = [
    "textsearch>=0.0.21",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "ruff>=0.1.0",
    "mypy>=1.0",
]
```

## Lockfile Support

To use uv's lockfile feature for reproducible builds:

```bash
# Generate lockfile
uv pip compile pyproject.toml -o requirements.lock

# Install from lockfile
uv pip sync requirements.lock
```

## CI/CD with uv

Update your GitHub Actions:

```yaml
- name: Install uv
  uses: astral-sh/setup-uv@v1
  
- name: Install dependencies
  run: uv pip install -e ".[dev]"
  
- name: Run tests
  run: pytest tests/
```

## More Information

- uv documentation: https://github.com/astral-sh/uv
- Package repository: https://github.com/devjerry0/sane-contractions

