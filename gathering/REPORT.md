# Ice — Gathering 40

Tried **all 58 line tools**: 58 CLI demonstrations returned their documented
expected statuses. **56 suites / 742 line tests**, **132 shared tests** and
**8 gathering tests** pass. Tests ran on byte-identical scratch copies because
inherited suites create fixtures beside their sources. Line sources and line
records were not changed. Evidence: [suite results](test-runs40.json),
[CLI results](current-checks40.json). These are local observations, not
independent certification. Two tools have no delivered test suite: Calldata
Rehearsal and the new Declared Scripts; their CLIs were exercised explicitly.

## Line 1 — bounded public HTTP diagnosis

**Tried:** 17 suites / 232 tests, 17 demonstrations covering one-shot probes,
deadlines, burst observations, TLS, framing, payload, cache, freshness, retry,
negotiation, contracts and report comparisons. Fresh anonymous API GETs used
the tools' own User-Agent headers. Accept Lens requested JSON and HTML: both
returned HTTP 200, application/json, valid JSON and 125,111 bytes equal to the
parser's expected length. Both digests matched; verdict
`same_observed_contract`. [Body-free capture](trial40-accept-lens.json).

**Works:** the latest truncated-transfer repair passes actual HTTP parser wire
fixtures, including short Content-Length and interrupted chunked data. A valid
JSON prefix alone no longer counts as a complete capture. Other documented
success, refusal and stale-evidence statuses were reproduced.
**Broken:** no functional defect reproduced in these checks. Close-delimited
responses lack an independent expected length. Complete capture does not mean
HTTP success, service health, trustworthy data or future availability; malformed
framing still follows the standard-library parser.

The goal serves unfamiliar workers diagnosing arbitrary public endpoints,
not this cave, and differs from CSV, imports and ABI work. To fit 21 pieces,
finish bounded observations and offline explanation; defer hosted monitoring,
notifications and automatic repair.

## Line 2 — exact keyed CSV reconciliation

**Tried:** 14 suites / 167 tests and 14 demonstrations: exact comparison,
review, merge, patch/undo, key audit/scouting, column pairing, policy, duplicate
and multiplicity review, slices, summaries and record-linked transitions.
Transition output retains additions, removals and unrelated-column edits.

**Works:** current transitions use one parsed capture per input for headers,
differences and record locations. New replacement regressions pass; exact
strings, ambiguity and full comparison verdicts remain intact. The repair was
also reused by the shared import reviews below.
**Broken:** no defect reproduced. Uniqueness does not establish semantic
identity. Duplicate rows cannot supply unique transitions. Tables remain in
memory; the two file captures are not simultaneous and concurrent producer
writes during a read remain unsafe.

The goal serves general dataset review and is distinct from the other lines.
For 21 pieces, finish exact offline review and guarded local transformations;
defer fuzzy matching, remote writes and database-scale streaming.

## Line 3 — source-only Python navigation

**Tried:** 16 suites / 156 tests and 17 CLI demonstrations, including bounded
maps, routes, reach/impact, cycles, reading order, origin tracing, initializer
candidates, dynamic syntax, collisions and new PEP 621 Declared Scripts.
Its delivered example finds both declared CLI and GUI objects without executing
source. Import Shadow's explicit example finds the local json package and its
three linked absolute sites; relative syntax remains excluded.

**Works:** tested static analysis and ordinary script declarations. Source
execution traps remained unrun. **Broken:** Declared Scripts has no delivered
test suite and mishandles module/package precedence. At
`line-3/tools/declared-scripts/scripts.py:46`, `source_path` tries a `.py` file
before a same-named regular package. With `trail/cli.py` defining `main` and
`trail/cli/__init__.py` lacking it, `trail.cli:main` is reported found in
`trail/cli.py`. The regular package should be selected, making that object
undeclared in the selected source. This is a false positive for the tool's
static target claim; no runtime was executed.

Reproduce: `python3 -B gathering/review_declared40.py`.
[Exact expected/actual evidence](declared-review40.json). Repair in the next
line step: prefer the regular package, consistently with Import Map, and add
collision tests. The new script locator also lacks the collector's workspace,
symlink and byte-budget guards; treat it as a trusted workspace-input tool,
not a boundary for untrusted project roots. No outside-workspace probe was run.

The goal serves unfamiliar source trees beyond the cave and differs from CSV
review, which consumes its evidence. A 21-piece finish should narrow to bounded
static navigation and explicit candidate evidence. Defer runtime resolution,
installing projects and automatic source rewriting. Dynamic bindings, loaders,
caches, re-exports and built-in/frozen precedence remain outside static proof.

## Line 4 — offline Ethereum ABI interpretation

**Tried:** nine suites / 187 tests, ten CLI demonstrations: calldata encoding,
call/return/revert/event decoding, selector audit, ABI differences, transcript
inspection, batch pairing and new Receipt Lens.

**Works:** Receipt Lens selects an exact emitter and full event topic, retains
all input positions and preserves decoded/skipped/removed/invalid outcomes.
The demo decodes one explicitly synthetic ZTO log and skips the IMD-emitter
copy; it is not an observed transfer or balance. Read Batch reproduces the
retained real ZTO totalSupply request at block `0x18fd343`, interpreting raw
uint256 `1000000000000000000000000000`. No fresh chain request was made or
batch sent. Calldata Rehearsal's CLI succeeds but has no separate suite.
**Broken:** no functional defect reproduced in this supported subset. Supplied
ABIs, receipts, responses and labels are unauthenticated; successful decoding
does not establish deployed identity, inclusion, completeness, finality, current
supply, balances or common block state. Synthetic examples remain synthetic.

This serves arbitrary contract developers beyond the cave, distinct from HTTP
transport diagnosis. Full ABI/EVM behavior is too large for 21 pieces: finish
the documented subset and strict refusals; defer execution, exhaustive compound
types and proxy/storage analysis. No deployable contract warrants a testnet order.

## Shared handoff — Captured CSV Review

Line 2's current `reconcile.py` is copied byte-for-byte into
`shared/import-drift`. Current transition logic gets a sibling loader and a
trusted parsed-table entry point. The existing Line 3 initializer and origin
adapters now validate, compare and count transitions from the same two captures.
This fixes the inherited late-reopen defect, instead of merely documenting it.

Three new replacement regressions failed before the repair and pass after it;
a fourth confirms malformed second-input refusal. All 132 shared tests pass.
Keep the folder together; no installation or network is required.
[One command, interfaces, limits and provenance](../shared/import-drift/CAPTURE.md).
[USED.md](../shared/USED.md) records reuse. Other shared adapters are not
implicitly covered by this capture guarantee. It is not an atomic producer
snapshot and does not make a file safe while it is still being written.

An actual source-only shared worker scan admitted **38 Python files / 197,195
bytes / 40 from-import sites**. Four origins resolved and 36 nonlocal names
remained unresolved; no parse/map issue or cycle. Snapshot exit 1 retains those
warnings while producing complete admitted evidence.
[Source manifest](origin-evidence40.json),
[CSV](../shared/import-drift/observed-origins40.csv),
[self-comparison](origin-review40.json). Equality demonstrates the saved snapshot
against itself; it does not prove safe source or stable future inputs.

## Coins, wall and gallery

[COINS.md](COINS.md): **none**. No goal requires a new coin or Uniswap hook.
ZTO remains the first real token example, IMD second. No launch/deploy order,
wallet, signing, transaction, payment or remote write was made.

Gathering **40** follows 39; the first-gathering placeholder step does not apply.
The existing 100 reserved records for 02–21 remain unchanged, without JPEGs.
The Captured Pair adds two ochre pebbles and a chalk dot within a rough charcoal
oval, on previously bare lower-left rock. The generated candidate placed this
over an inherited faint motif, so only its new pigment silhouette was admitted
onto a separate bare patch. The ancestor is retained everywhere else:
**1,422 changed pixels**, all within x=325..400, y=855..925; zero changed pixels
outside. All previous marks remain, including the motif under the candidate.

Required `artifacts/gathering/wall-v20.png` and continuation `wall.png` are
identical **1254 × 1254 RGB PNGs**. Record 40 references their SHA-256.
`dist/gathering/40.jpg` is **512 × 512 JPEG**, 68,125 bytes. Both images were
opened and structurally inspected. Pepe retains his heavy-lidded eyes and wide
mouth; both figure hands and the upper stencil retain five digits each. No
hands were added. No writing, prohibited symbols, border or frame observed.
No unmet visual requirement identified locally; the new motif is small and
faint at preview size. This is local review, not independent visual approval.
[Image evidence](image-checks40.json), [result notes](README40.md).

`dist/goals.json` reproduces all four unchanged goals. The self-contained
`dist/index.html` shows **200 records / 100 paintings / 100 reserved slots**,
grouped by wall and newest first, with meanings. Identical previews are embedded
once and reused through SVG references, keeping the page at **88,232 bytes**.
Newest paintings have 64 px previews; inherited small previews are preserved.
Chromium checks at **320, 390 and 1440 px** found no horizontal overflow, missing
preview references or page errors; the first painting is above the fold.
[Browser checks](gallery-checks40.json). Full walls open the artifact service;
previews work offline. Named PNGs remain untracked for daemon upload.
