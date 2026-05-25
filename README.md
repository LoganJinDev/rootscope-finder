# rootscope-finder

A lightweight, dependency-free project root finder for Python and CLI usage.

## Why

This package discovers a project root by walking upward from a start path and matching common project marker files/directories (for example `.git`, `pyproject.toml`, `package.json`).

## Install

### From PyPI

```bash
pip install rootscope-finder
```

### From GitHub

```bash
pip install "git+https://github.com/LoganJinDev/rootscope-finder.git"
```

## CLI

```bash
find-root
find-root /path/to/any/subdir
find-root /tmp --strict
find-root --json
```

## Python API

```python
from rootscope_finder import find_project_root, require_project_root

root = find_project_root()
# or
root = require_project_root()
```

## Python Usage Examples

```python
from rootscope_finder import find_project_root

# Find from current dir
root = find_project_root()

# Start from a specific path
root = find_project_root(path="assets/images")

# Limit search depth
root = find_project_root(max_depth=3)

# Use custom markers
root = find_project_root(markers=[".git", "pyproject.toml", "requirements.txt"])

# Combine options
root = find_project_root(
    path="src",
    max_depth=5,
    markers=["manifest.json"],
)

# Priority search by project name (searches only in provided workspace roots)
root = find_project_root(
    project_name="TestProject",
    workspace_roots=["/Users/xxx/Desktop/LoganJinDev"],
)
```

## Behavior

- `PROJECT_ROOT` env var can override detection (default enabled).
- `--no-env` disables env override.
- `--marker` can add custom markers.
- `--strict` returns exit code `1` when not found.

## CLI Usage Examples

```bash
# Find from current dir
find-root

# Start from specific path
find-root assets/images

# Limit search depth
find-root --max-depth 3

# Add custom markers (repeat --marker)
find-root --marker .git --marker pyproject.toml --marker requirements.txt

# Combine options
find-root src --max-depth 5 --marker manifest.json

# Priority search by project name (no full-disk scan)
find-root --project-name TestProject --workspace-root /Users/xxx/Desktop/LoganJinDev
```

## Development

```bash
python -m pip install -e .
pytest
python -m build
```

## License

MIT

## Publish to PyPI

This repository includes `.github/workflows/publish-pypi.yml`.

1. In PyPI, create project `rootscope-finder` and configure Trusted Publisher for this GitHub repo.
2. Create and push a version tag:

```bash
git tag v0.1.1
git push origin v0.1.1
```

3. After workflow success, users can install directly:

```bash
pip install rootscope-finder
```
