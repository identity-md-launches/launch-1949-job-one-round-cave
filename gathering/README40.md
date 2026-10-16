# Gathering 40 — The Captured Pair

Delivered wall: `artifacts/gathering/wall-v20.png`, with identical continuation
`artifacts/gathering/wall.png`. PNG, RGB, 1254 × 1254, 4,017,207 bytes.
Preview: `dist/gathering/40.jpg`, JPEG, 512 × 512, 68,125 bytes.
Record: `dist/gathering/40.json`; image URL uses the full PNG's lowercase SHA-256.

The installed image editor generated two ochre pebbles, a chalk dot and a rough
charcoal enclosure. Its placement overlapped an old motif; the new pigment was
isolated and placed on bare lower-left rock using `finish_wall40.js`. Exactly
1,422 pixels change and no pixel outside x=325..400,y=855..925 changes. Existing
Pepe, five-digit hands, marks, rock, cracks, light and framing remain intact.
The source editor candidate was not kept as another workspace picture.

Opened the full wall and JPEG; structural image inspection passed. No unmet
visual requirement observed. The small mark is faint at 512 px. Local review
is not independent approval. Image-generation provenance and pixel evidence:
`image-checks40.json`. The finish script consumes the original editor candidate,
not its own finished output; it is retained for provenance, not as an idempotent
rebuild command.

Useful shared result: `shared/import-drift/CAPTURE.md`. It repairs source-review
consistency using Line 2's captured tables. Four new tests pass after reproducing
three failures before repair. All 742 line tests, 132 shared tests, eight
gathering tests and 58 CLI demonstrations pass. Declared Scripts' package/module
precedence defect is recorded for Line 3 in REPORT.md, with a reproducible input.

One offline command to see the shared result:

```sh
python3 -B shared/import-drift/origin_csv.py compare shared/import-drift/observed-origins39.csv shared/import-drift/observed-origins39.csv
```

One command to verify final delivery:

```sh
python3 -B gathering/check_delivery40.py
```

Gallery rebuild: `python3 -B gathering/build_gallery.py` (Python standard library,
Node and delivered JPEG codec only). Browser verification is optional local
tooling: `PLAYWRIGHT_BROWSERS_PATH=/opt/imd-tools/ms-playwright node gathering/check_gallery40.mjs`.
No runtime package is required by the self-contained gallery. No coin or
contract deployment is requested. Full details and limitations: REPORT.md.
