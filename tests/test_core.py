from pathlib import Path

from rootscope_finder import find_project_root, require_project_root


def test_find_project_root_from_nested_dir(tmp_path: Path):
    project = tmp_path / "demo"
    nested = project / "a" / "b" / "c"
    nested.mkdir(parents=True)
    (project / ".git").mkdir()

    root = find_project_root(nested)
    assert root == str(project.resolve())


def test_find_project_root_returns_none_if_missing_marker(tmp_path: Path):
    start = tmp_path / "x" / "y"
    start.mkdir(parents=True)

    assert find_project_root(start, use_env=False) is None


def test_require_project_root_raises(tmp_path: Path):
    start = tmp_path / "plain"
    start.mkdir()

    try:
        require_project_root(start, use_env=False)
        assert False, "expected RuntimeError"
    except RuntimeError:
        assert True


def test_env_override(tmp_path: Path, monkeypatch):
    env_root = tmp_path / "envroot"
    env_root.mkdir()
    monkeypatch.setenv("PROJECT_ROOT", str(env_root))

    result = find_project_root(tmp_path / "anything")
    assert result == str(env_root.resolve())


def test_project_name_priority_over_marker_search(tmp_path: Path):
    workspace = tmp_path / "workspace"
    target = workspace / "target-proj"
    target.mkdir(parents=True)

    other = tmp_path / "other"
    nested = other / "a" / "b"
    nested.mkdir(parents=True)
    (other / ".git").mkdir()

    result = find_project_root(
        path=nested,
        use_env=False,
        project_name="target-proj",
        workspace_roots=[workspace],
    )
    assert result == str(target.resolve())
