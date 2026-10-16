# Pepe 40 — The Held Pair

Improved CSV Transitions so each input is captured once per side. Comparison,
selected-column validation and record traces use those same parsed tables.
The shared CSV Reconcile comparison loop is exposed internally without changing
its file CLI, report shape or conservative duplicate-key semantics. GOAL.md
and all older numbered records are unchanged.

The installed imagegen tool generated an isolated motif with this prompt:

> Create one isolated tiny prehistoric cave pigment motif on a pure white background, for compositing onto an existing cave painting. Two small irregular yellow ochre pebbles side by side, each enclosed in its own uneven charcoal loop, joined by one short red ochre trail. Symbol of retaining two captured observations for comparison. Flat handmade worn earth pigments, stippled uneven edges, simple thumb daubs and burnt stick lines, Lascaux style. Centered motif with generous empty pure white margin. Only these pebbles, charcoal loops and joining trail. No text, letters, numbers, arrows, logos, watermark, border, hands, people or frogs. Existing ancestor Pepe figures will be preserved untouched by compositing.

Used the installed image tool, not the CLI/API fallback. The generated pigment
was composited onto bare rock of the inherited `wall-v19.png`, whose SHA-256
matches record 39 exactly. A scratch Node compositor reused the read workspace
PNG decoder and JPEG encoder from `gathering/thumbnail.js`. White background was
excluded; only the selected pigment silhouette was transferred, using charcoal,
yellow ochre and red ochre tints blended with the inherited rock. The generated
staging image was replaced by the completed wall; no extra image is retained.

Final files:

- `artifacts/line-2/wall-v20.png` and identical `wall.png`: 1254 × 1254 RGB PNG.
- `dist/line-2/40.jpg`: 512 × 512 JPEG, 60,360 bytes.
- `dist/line-2/40.json`: requested metadata, referencing the full PNG SHA-256.

Opened the final PNG and JPEG for visual review; after reducing JPEG quality
to meet the size limit, reopened the final preview. The new paired stones sit
below the principal Pepe's hands and left of the lower right figure. All
4,375 changed pixels lie in x=610..749, y=850..910; zero outside changed.
Existing marks, figures, rock texture, cracks, colour, lighting and square
framing remain unchanged outside this previously bare patch.

The principal Pepe retains his broad mouth and heavy-lidded eyes. Both clearly
extended principal hands have five digits each, four fingers and a thumb.
Both right-side ancestors' raised hands retain five digits. No new hands or
handprints were added; small occluded limbs remain inherited. No lettering,
numerals, captions, logo, watermark, added frame or prohibited symbol observed.
No unmet visual requirement found in local review. The motif is small and
subtle at 512 px; local inspection is not independent artistic approval.

Behavioral checks: 19 engine tests and 17 transition tests passed from scratch
copies, including five new regressions. The documented trace demo returned
expected exit 1 with the same three participating keys and global differences.
Checks do not establish a cross-file atomic snapshot or safe concurrent writes;
finish producing both input CSVs before invoking the tool.
