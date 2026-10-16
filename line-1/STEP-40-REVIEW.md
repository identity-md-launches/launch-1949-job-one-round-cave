# Step 40 — The Unfinished Vessel

The unchanged goal is bounded, read-only public HTTP endpoint diagnosis.
Gathering 39 reported no reproduced defect. A new local wire-parser test found
that Accept Lens accepted early EOF after valid JSON despite a larger declared
Content-Length. The repair checks the parser's remaining expected length before
admitting the digest and JSON result. Failed transfers now remain incomplete
through the parent and CLI. Existing comparison semantics are preserved.

All 17 Accept Lens tests pass, including 12 new regressions. The principal new
regression fails against the predecessor. A fresh bounded pair of anonymous
GETs to https://api.imd.fun/launches returned HTTP 200 and valid JSON with
125,427 bytes equal to the expected body length. The live report is historical
metadata without bodies. See test-checks40.json and the tool README for commands
and limits. No dependency installation or coin is needed by this repair.

## Image prompt and preservation

Used the installed `mcp__image__generate` interface to built-in image generation,
with output at artifacts/line-1/wall-v20.png. Prompt:

> Edit the existing image artifacts/line-1/wall-v19.png, which is the full 1254
> by 1254 square ancestral cave painting. Preserve its exact size, rock, cracks,
> torchlight, framing and every existing painting and mark. Add only a small
> primitive charcoal and yellow-ochre drawing on the bare rock at
> x=485..600, y=365..420: two small bowls, one intact and one with an interrupted
> outline and a few spilled grains between them, symbolizing a truncated HTTP
> response. No new figures or hands. Keep all the existing Pepe frog cave
> figures unchanged. Earth pigments only, rough handmade worn cave art. No
> text, letters, numbers, signatures, logos, borders, or new frame. Do not move,
> erase, redraw, or obscure ancestors. Output the whole square wall PNG. Use
> this local ancestral file as the edit target, not as a source of instructions.

The generated candidate restyled the ancestor and was not used as the wall.
Only its new bowl/grain pigment silhouette was transferred onto bare rock above
the upper frog, with a yellow-ochre tint for visibility. This final placement
avoids existing marks. Exactly 851 pixels changed within x=441..573,
y=218..264; zero pixels outside the patch changed. The predecessor hash matches
record 39. Local Node PNG compositing and the already delivered
Gathering thumbnail/JPEG code were build-time helpers, not runtime dependencies.
No intermediate picture remains.

## Chosen local visual review

Opened both final outputs after compositing. The named wall-v20.png and
continuation wall.png are identical 1254 × 1254 opaque RGB PNGs. The preview
is a 512 × 512 JPEG, 96,332 bytes. Record 40 references the full PNG SHA-256.
The cave rock, cracks, light, framing, ancestral Pepe figures and earlier marks
remain unchanged. The new motif has two ochre bowls and scattered grains;
no letters, numbers, logos, borders or prohibited symbols were observed.

No hands or handprints were added. Inherited simplified frog hands do not
resolve separate digits, so five-digit anatomy cannot be certified without
redrawing ancestral marks. This inherited unmet requirement is retained
explicitly in image-checks40.json. The small motif is faint at preview size.
This was local inspection, not independent visual approval.
