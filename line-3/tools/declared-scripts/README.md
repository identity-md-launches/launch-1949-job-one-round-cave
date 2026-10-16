# Declared Scripts

Read PEP 621 `project.scripts` and `project.gui-scripts` declarations in a
`pyproject.toml`, resolve each dotted module beneath a chosen source root, and
check whether the target object is statically declared in that file. It parses
metadata and Python syntax only; it never imports or executes project code.

Run the example from the repository root with Python 3.11 or newer (for the
standard-library `tomllib` parser), fully offline:

```sh
python3 -B line-3/tools/declared-scripts/scripts.py line-3/tools/declared-scripts/examples/pyproject.toml --root line-3/tools/declared-scripts/examples/src
```

When tried, this reports `trail -> module_and_object_found` at `trail/cli.py`
and `trail-window -> module_and_object_found` at `trail/gui.py`. The GUI example
contains an execution trap; it remained unexecuted. Run with `--json` for a
machine-readable report.

This recognizes only PEP 621 metadata; legacy `setup.cfg`, `setup.py`,
workspace-specific configuration, dynamic metadata, editable installs and
plugin discovery are outside scope. A target object is checked among direct
module definitions and nested class definitions; imported/re-exported objects
may therefore be reported as not declared. A matching source and object do
not prove that the command installs or runs successfully. Python 3.11+ is
required. No package, network, coin, wallet or chain state is needed.
