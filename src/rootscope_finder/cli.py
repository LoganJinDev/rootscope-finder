"""CLI entrypoint for rootscope-finder."""

from __future__ import annotations

import argparse
import json

from .core import find_project_root


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Find project root from any directory")
    parser.add_argument("path", nargs="?", default=None, help="start path (default: cwd)")
    parser.add_argument("--max-depth", type=int, default=None, help="max parent levels to walk")
    parser.add_argument("--marker", action="append", default=None, help="extra marker (repeatable)")
    parser.add_argument("--project-name", default=None, help="fallback: locate project by directory name")
    parser.add_argument(
        "--workspace-root",
        action="append",
        default=None,
        help="workspace root to search with --project-name (repeatable)",
    )
    parser.add_argument(
        "--name-search-max-depth",
        type=int,
        default=6,
        help="max depth per workspace root for --project-name search",
    )
    parser.add_argument(
        "--workspace-roots-env-var",
        default="ROOTSCOPE_WORKSPACE_ROOTS",
        help="env var containing workspace roots separated by os.pathsep",
    )
    parser.add_argument("--env-var", default="PROJECT_ROOT", help="environment override variable")
    parser.add_argument("--no-env", action="store_true", help="disable environment override")
    parser.add_argument("--strict", action="store_true", help="return exit code 1 when not found")
    parser.add_argument("--json", action="store_true", help="output as JSON")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    root = find_project_root(
        path=args.path,
        max_depth=args.max_depth,
        extra_markers=args.marker,
        env_var=args.env_var,
        use_env=not args.no_env,
        project_name=args.project_name,
        workspace_roots=args.workspace_root,
        workspace_roots_env_var=args.workspace_roots_env_var,
        name_search_max_depth=args.name_search_max_depth,
    )

    if args.json:
        print(json.dumps({"project_root": root}, ensure_ascii=False))
    else:
        print(root)

    if args.strict and root is None:
        return 1
    return 0
