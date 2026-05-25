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
    )

    if args.json:
        print(json.dumps({"project_root": root}, ensure_ascii=False))
    else:
        print(root)

    if args.strict and root is None:
        return 1
    return 0
