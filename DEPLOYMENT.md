# Deployment Guide

## Modern Approach (Recommended): GitHub Actions

The package uses automated GitHub Actions for releases.

### Process:

1. **Create a release on GitHub:**
   ```bash
   git tag v0.1.73
   git push origin v0.1.73
   ```

2. **Create GitHub Release:**
   - Go to GitHub → Releases → "Create a new release"
   - Choose the tag you just created
   - Write release notes
   - Click "Publish release"

3. **Automatic deployment:**
   - GitHub Actions will automatically:
     - Update version based on commit count
     - Build the package
     - Run tests
     - Publish to PyPI

### Configuration:

The workflow is in `.github/workflows/publish.yml`

**Required secrets** (configure in GitHub Settings → Secrets):
- PyPI now uses trusted publishers - no token needed!
- Configure at: https://pypi.org/manage/account/publishing/

## Legacy Approach: Manual Script

For manual releases, you can use `deploy.py`:

### Prerequisites:

```bash
pip install build twine
```

### Steps:

1. **Run the deployment script:**
   ```bash
   python deploy.py
   ```

2. **The script will:**
   - Count git commits for version
   - Update setup.py and __init__.py
   - Build distribution files
   - Ask for confirmation
   - Upload to PyPI

### First time setup:

Create `~/.pypirc`:
```ini
[pypi]
username = __token__
password = pypi-YOUR-TOKEN-HERE
```

## Version Scheme

The package uses an automatic versioning scheme:

```
MAJOR.MINOR.MICRO
```

- **MAJOR**: Set manually in `setup.py` (breaking changes)
- **MINOR**: Set manually in `setup.py` (new features)
- **MICRO**: Auto-generated from git commit count

Example: `0.1.325` means version 0.1 with 325 total commits

## Testing Before Release

Always test locally before deploying:

```bash
# Run all tests
pytest tests/ -v

# Check coverage
pytest tests/ --cov=contractions

# Run linting
ruff check .
mypy contractions/ tests/

# Build locally to test
python -m build
```

## Rollback

If a release has issues:

1. Delete the git tag:
   ```bash
   git tag -d v0.1.73
   git push origin :refs/tags/v0.1.73
   ```

2. Fix the issue and create a new release

