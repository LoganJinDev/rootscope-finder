"""Core root-discovery logic."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable

from .markers import DEFAULT_MARKERS


def _normalize_start(path: str | os.PathLike[str] | None) -> Path:
    start = Path.cwd() if path is None else Path(path).expanduser()
    if not start.exists():
        raise ValueError(f"Path does not exist: {start.resolve()}")
    if start.is_file():
        start = start.parent
    return start.resolve()


def _iter_ancestors(start: Path, max_depth: int | None):
    current = start
    depth = 0
    while True:
        yield current
        if max_depth is not None and depth >= max_depth - 1:
            return
        parent = current.parent
        if parent == current:
            return
        current = parent
        depth += 1


def find_project_root(
    path: str | os.PathLike[str] | None = None,
    *,
    markers: Iterable[str] | None = None,
    extra_markers: Iterable[str] | None = None,
    max_depth: int | None = None,
    env_var: str = "PROJECT_ROOT",
    use_env: bool = True,
) -> str | None:
    """Find project root by walking upward and matching marker names."""
    if max_depth is not None and max_depth <= 0:
        raise ValueError("max_depth must be > 0 or None")

    if use_env:
        env_value = os.getenv(env_var)
        if env_value:
            env_path = Path(env_value).expanduser()
            if env_path.is_dir():
                return str(env_path.resolve())

    marker_set = set(DEFAULT_MARKERS if markers is None else markers)
    if extra_markers:
        marker_set.update(extra_markers)

    start = _normalize_start(path)

    for directory in _iter_ancestors(start, max_depth=max_depth):
        try:
            names = set(os.listdir(directory))
        except OSError:
            return None
        if marker_set & names:
            return str(directory)

    return None


def require_project_root(
    path: str | os.PathLike[str] | None = None,
    **kwargs,
) -> str:
    """Same as find_project_root but raises when root is not found."""
    root = find_project_root(path=path, **kwargs)
    if root is None:
        raise RuntimeError("Project root not found")
    return root
