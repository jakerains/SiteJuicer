# SiteJuicer Development Guidelines

This document outlines important rules and workflows for maintaining and updating the SiteJuicer project, particularly regarding version management and synchronization between GitHub and PyPI.

## Version Management

SiteJuicer follows semantic versioning (`MAJOR.MINOR.PATCH`):

- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality in a backward-compatible manner
- **PATCH**: Backward-compatible bug fixes

### Updating the Version

When making changes that require a new version:

1. Update the version in `sitejuicer/__init__.py`:
   ```python
   __version__ = '0.2.1'  # Change to new version
   ```

2. The `pyproject.toml` uses dynamic versioning, so it will automatically use the version from `__init__.py`.

3. Update the `CHANGELOG.md` with details about the new version.

## Release Process

### Automatic Deployment to PyPI

The project is configured to automatically deploy to PyPI in two scenarios:

1. When a GitHub Release is created
2. When a tag starting with 'v' is pushed (e.g., `v0.2.2`)

### Steps for a New Release

1. **Update the Version and CHANGELOG**
   ```bash
   # Edit sitejuicer/__init__.py to update version
   vim sitejuicer/__init__.py
   
   # Update CHANGELOG.md with new version details
   vim CHANGELOG.md
   ```

2. **Commit Changes and Create a Tag**
   ```bash
   git add sitejuicer/__init__.py CHANGELOG.md
   git commit -m "Bump version to X.Y.Z"
   git tag -a vX.Y.Z -m "Release version X.Y.Z"
   git push origin main --tags
   ```

3. **Create a GitHub Release (Optional but Recommended)**
   - Go to the GitHub repository
   - Navigate to "Releases"
   - Click "Draft a new release"
   - Select the tag you just created
   - Add a title and description
   - Click "Publish release"

### Important Notes

- **The GitHub Actions workflow will automatically build and publish the package to PyPI** when a new tag starting with 'v' is pushed or a release is created.
- **Always test your changes thoroughly before releasing a new version**.
- The PyPI API token must be configured as a secret in the GitHub repository settings.

## Required GitHub Secrets

- `PYPI_API_TOKEN`: Token for publishing to PyPI

## Common Issues

### Version Conflicts

If you encounter version conflicts or unexpected behavior:

1. Ensure the version in `__init__.py` has been updated.
2. Check if the tag names match the version correctly.
3. Verify the GitHub Action logs for any deployment issues.

### Manual PyPI Publication

If automatic publication fails, you can publish manually:

```bash
# Build the package
python -m build

# Upload to PyPI
twine upload dist/*
```

## Testing Before Release

Always run the full test suite before releasing:

```bash
# Run tests
pytest

# Run type checking
mypy sitejuicer

# Check code style
flake8 sitejuicer
black --check sitejuicer
isort --check sitejuicer
``` 