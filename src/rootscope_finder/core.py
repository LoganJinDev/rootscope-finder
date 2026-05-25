"""Core root-discovery logic."""

from __future__ import annotations

import os
from collections import deque
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


def _iter_subdirs_with_depth(root: Path, max_depth: int):
    queue: deque[tuple[Path, int]] = deque([(root, 0)])
    while queue:
        current, depth = queue.popleft()
        if depth >= max_depth:
            continue
        try:
            with os.scandir(current) as entries:
                for entry in entries:
                    if not entry.is_dir(follow_symlinks=False):
                        continue
                    child = Path(entry.path)
                    yield child, depth + 1
                    queue.append((child, depth + 1))
        except OSError:
            continue


def _resolve_workspace_roots(
    workspace_roots: Iterable[str | os.PathLike[str]] | None,
    workspace_roots_env_var: str,
) -> list[Path]:
    roots: list[Path] = []

    if workspace_roots:
        for item in workspace_roots:
            if item is None:
                continue
            path = Path(item).expanduser()
            if path.is_dir():
                roots.append(path.resolve())
        return roots

    env_value = os.getenv(workspace_roots_env_var, "")
    if not env_value:
        return roots

    for raw in env_value.split(os.pathsep):
        raw = raw.strip()
        if not raw:
            continue
        path = Path(raw).expanduser()
        if path.is_dir():
            roots.append(path.resolve())
    return roots


def _find_by_project_name(
    project_name: str,
    workspace_roots: Iterable[str | os.PathLike[str]] | None,
    workspace_roots_env_var: str,
    name_search_max_depth: int,
) -> str | None:
    target = project_name.strip()
    if not target:
        return None

    roots = _resolve_workspace_roots(workspace_roots, workspace_roots_env_var)
    for root in roots:
        if root.name == target:
            return str(root)
        for candidate, _depth in _iter_subdirs_with_depth(root, max_depth=name_search_max_depth):
            if candidate.name == target:
                return str(candidate.resolve())
    return None


def find_project_root(
    path: str | os.PathLike[str] | None = None,
    *,
    markers: Iterable[str] | None = None,
    extra_markers: Iterable[str] | None = None,
    max_depth: int | None = None,
    env_var: str = "PROJECT_ROOT",
    use_env: bool = True,
    project_name: str | None = None,
    workspace_roots: Iterable[str | os.PathLike[str]] | None = None,
    workspace_roots_env_var: str = "ROOTSCOPE_WORKSPACE_ROOTS",
    name_search_max_depth: int = 6,
) -> str | None:
    """Find project root by env, ancestor markers, then optional project-name fallback."""
    if max_depth is not None and max_depth <= 0:
        raise ValueError("max_depth must be > 0 or None")
    if name_search_max_depth <= 0:
        raise ValueError("name_search_max_depth must be > 0")

    if use_env:
        env_value = os.getenv(env_var)
        if env_value:
            env_path = Path(env_value).expanduser()
            if env_path.is_dir():
                return str(env_path.resolve())

    if project_name:
        found = _find_by_project_name(
            project_name=project_name,
            workspace_roots=workspace_roots,
            workspace_roots_env_var=workspace_roots_env_var,
            name_search_max_depth=name_search_max_depth,
        )
        if found is not None:
            return found

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
