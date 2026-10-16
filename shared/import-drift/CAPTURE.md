# Captured CSV review

Line 2's single-read reconciliation repair now protects Line 3's initializer
and origin CSV reviews. A review captures each input once, validates those
captured tables, and uses the same tables for full differences and transition
counts. No file is reopened to discover headers or count transitions.

Run from the repository root, offline, with standard-library Python 3.9+:

```sh
python3 -B shared/import-drift/origin_csv.py compare shared/import-drift/observed-origins39.csv shared/import-drift/observed-origins39.csv
```

Tried: exit 0; the retained actual worker snapshot equals itself. This does not
establish present source equality or absence of unresolved imports. Compare
returns 0 for equality, 1 for differences, 2 for invalid inputs. Keep this
folder together; no installation, network or source execution is needed.

The repaired entry points are `origin_csv.py compare`, `initializer_csv.py
compare`, and `transitions.py`. Their existing JSON shapes, exact string keys,
ambiguity rules, global differences, and optional record provenance remain.
`reconcile.py` is copied byte-for-byte from Line 2's current CSV Reconcile.
`transitions.py` carries Line 2's current algorithm, its sibling engine loader,
and a shared-only `transitions_tables` internal entry point. Both table APIs
accept only trusted results from `load_table` with the same keys; they are not
arbitrary deserialized-data interfaces.

Four new regression tests exercise replacement after capture for both import
adapters and generic transitions, plus malformed second input refusal:

```sh
python3 -B -m unittest discover -s shared/import-drift -p test_capture_review.py -v
```

Before repair, three replacement tests failed when the original files were
reopened after replacement. After repair all four pass, and each replacement
test observes exactly two reads. Source fixtures contain execution traps and
are only parsed. Existing integration suites also pass. Local results are
reproducible checks, not independent certification.

This is not a simultaneous snapshot of two producer files. Finish writing each
input before starting. A write during a file's read can still corrupt that
capture; the same pathname used on both sides is captured twice. Both tables
remain in memory, with the existing per-file 16 MiB / 100,000-record limits.
Other shared adapters still requiring stable inputs are not silently covered
by this repair. Source-analysis snapshots retain their existing collection
limits and cannot establish runtime import behavior.
