#!/usr/bin/env python3
"""Inspect PEP 621 CLI declarations without importing project code."""
import argparse
import ast
import json
import re
import sys
import tomllib
from pathlib import Path


TARGET = re.compile(r"^([A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*):([A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*)$")


def declared_scripts(pyproject):
    """Return normalized script declarations or raise ValueError on bad metadata."""
    try:
        data = tomllib.loads(Path(pyproject).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, tomllib.TOMLDecodeError) as exc:
        raise ValueError("cannot read valid UTF-8 TOML: " + str(exc)) from exc
    project = data.get("project", {})
    if not isinstance(project, dict):
        raise ValueError("[project] must be a table")
    result = []
    for group in ("scripts", "gui-scripts"):
        entries = project.get(group, {})
        if not isinstance(entries, dict):
            raise ValueError("[project." + group + "] must be a table")
        for name, target in sorted(entries.items()):
            if not isinstance(target, str):
                raise ValueError("script target for " + name + " must be a string")
            match = TARGET.fullmatch(target)
            if not match:
                result.append({"group": group, "name": name, "target": target,
                               "status": "unsupported_target_syntax"})
            else:
                result.append({"group": group, "name": name, "target": target,
                               "module": match.group(1), "object": match.group(2),
                               "status": "unresolved"})
    return result


def source_path(root, module):
    base = Path(root)
    parts = module.split(".")
    candidates = (base.joinpath(*parts).with_suffix(".py"),
                  base.joinpath(*parts, "__init__.py"))
    for path in candidates:
        if path.is_file():
            return path
    return None


def declared_objects(tree):
    """Collect top-level definitions and directly nested class/function names."""
    names = set()
    def visit(body, prefix=""):
        for node in body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                full = prefix + node.name
                names.add(full)
                if isinstance(node, ast.ClassDef):
                    visit(node.body, full + ".")
            elif isinstance(node, (ast.Assign, ast.AnnAssign)):
                targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                for target in targets:
                    if isinstance(target, ast.Name):
                        names.add(prefix + target.id)
    visit(tree.body)
    return names


def inspect(pyproject, root):
    entries = declared_scripts(pyproject)
    for item in entries:
        if "module" not in item:
            continue
        path = source_path(root, item["module"])
        if path is None:
            item["status"] = "module_not_found"
            continue
        item["source"] = path.relative_to(Path(root)).as_posix()
        try:
            source = path.read_bytes()
            tree = ast.parse(source, filename=str(path))
        except (OSError, SyntaxError, ValueError) as exc:
            item["status"] = "source_unreadable_or_invalid"
            item["detail"] = str(exc).splitlines()[0]
            continue
        item["object_declared"] = item["object"] in declared_objects(tree)
        item["status"] = "module_and_object_found" if item["object_declared"] else "module_found_object_not_declared"
    return {"pyproject": str(pyproject), "source_root": str(root),
            "execution": "none", "scripts": entries}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pyproject", help="path to pyproject.toml")
    parser.add_argument("--root", required=True, help="source root for dotted modules")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    args = parser.parse_args(argv)
    try:
        report = inspect(args.pyproject, args.root)
    except ValueError as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        if not report["scripts"]:
            print("No PEP 621 scripts declared.")
        for item in report["scripts"]:
            print(item["name"] + " (" + item["group"] + "): " + item["target"] +
                  " -> " + item["status"] + (" at " + item["source"] if "source" in item else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
