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

## Behavior

- `PROJECT_ROOT` env var can override detection (default enabled).
- `--no-env` disables env override.
- `--marker` can add custom markers.
- `--strict` returns exit code `1` when not found.

## Development

```bash
python -m pip install -e .
pytest
python -m build
```

## License

MIT
