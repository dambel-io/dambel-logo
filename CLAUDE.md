# CLAUDE.md

Asset-generation repo for the **Dambel** logo (Dambel: fitness/nutrition product; the logo is a dumbbell mark). There is no application code — one Python script assembles SVG fragments into logo variants and renders them to PNG at every required size. The rendered files in `output/` are **committed on purpose** (they are linked and previewed from the README on GitHub).

## Commands

```shell
python3 -m venv .venv && source .venv/bin/activate   # once
pip install -r requirements.txt                       # once (CairoSVG needs the cairo system library)
python3 generate.py                                   # regenerate everything in output/ + the README variant list
```

There are no tests. Verification = run `generate.py` and confirm the diff in `output/` is only what you intended (PNGs are binary; compare pixels, not bytes, when in doubt).

## How generation works (`generate.py`)

1. Loads the SVG fragments from `assets/` as plain text (see `FRAGMENT_NAMES`).
2. For each entry in `VARIANTS`, splices fragments into a base template by **plain string substitution** — no XML parsing:
   - `<!-- Background -->` placeholder ← `background.svg` (square) / `rounded.svg` / `circle.svg`, or left as-is for transparent variants.
   - `<!-- Dumbbell -->` placeholder ← `dumbbell.svg` (or `dumbbell_tight.svg` for tight variants).
   - `{background_color}` / `{dumbbell_color}` tokens ← values from `COLORS` (`gradient` → `url(#bgGradient)`, `dark` → `#383838`, `white` → `#ffffff`).
3. Writes `output/<variant>.svg`, renders it with `cairosvg.svg2png` at natural size, then resizes that master PNG with Pillow (`Image.resize` with an explicit `Image.Resampling.BICUBIC` filter — this is also Pillow's default, so making it explicit does not change the output bytes) to every entry in `SIZES` → `output/<variant>_<N>x<N>.png`.
4. Rewrites `README.md` below the `## Variants` marker with the full variant/file list.

### Variant model

A `Variant` = background shape (`background`/`rounded`/`circle` fragment, or `None` for transparent) + background color + dumbbell color + optional `tight`. Naming convention: `<shape>_<bg-color>` uses the default contrasting dumbbell (dark on gradient, gradient on dark); the `_white` suffix forces a white dumbbell. `dumbbell_*` variants are mark-only (no background); `*_tight` uses the cropped template.

**Note the one place fragment name ≠ variant prefix:** the square background fragment is `assets/background.svg`, but its variants are named **`full_*`** (`full_gradient`, `full_dark`, …) — only `rounded` and `circle` reuse their fragment name as the prefix. So "full" in an output filename means the square/full-bleed background, and a grep for `background` will not find those variants.

## Coordinate system & rendering facts (don't break these)

- `assets/base.svg`: 1600pt × 1600pt, `viewBox="0 0 1600 1600"`. CairoSVG renders pt at 96 dpi → the master PNGs are **2133×2133 px**. All PNG sizes are downscales of this one render.
- `assets/base_tight.svg`: same canvas but `viewBox="200 200 1200 1200"` with `preserveAspectRatio="xMidYMid slice"` — it crops the whitespace around the mark. It has **no** `<!-- Background -->` placeholder; tight variants are always transparent.
- `assets/dumbbell.svg` / `dumbbell_tight.svg`: identical path data (a `<g>` with `transform="translate(0,1600) scale(0.1,-0.1)"` — Y-flipped, coordinates in a 16000-unit space). If you edit the mark, edit **both** files.
- The `bgGradient` linearGradient (`#F66B34` → `#F99C78`, 135°) is defined in each base template's `<defs>`; the gradient color token resolves to `url(#bgGradient)`, so the def must exist in any template.
- Brand colors: gradient `#F66B34 → #F99C78`, dark `#383838`, white `#ffffff`. `banner.html` reuses the same two gradient stops for the tagline banner (standalone file, not part of generation) but at **90° (horizontal), not the logo's 135°** — deliberate: the gradient is clipped to a single wide line of text (696×118), where a diagonal ramp would read as uneven brightness across the words. Keep the stops in sync with the brand colors above; the angle is intentionally allowed to differ.

## Editing rules

- **Never hand-edit anything in `output/`** — it is 100% regenerated. `.claude/settings.json` enforces this for agents by denying `Edit(output/**)`/`Write(output/**)`, so `output/` can only change via `generate.py`. Same for `README.md` below the `## Variants` line (the marker string is load-bearing; `update_readme` splits on it). Prose above the marker is safe to edit.
- After changing anything in `assets/`, `VARIANTS`, `SIZES`, or `COLORS`, run `generate.py` and commit the regenerated `output/` + `README.md` together with the source change.
- Fragments are spliced as raw text: keep the placeholder comments and `{…_color}` tokens exactly as spelled, don't add XML prologs to fragment files (only the two `base*.svg` templates are complete SVG documents), and don't introduce duplicate element ids.
- Adding a variant: add a `Variant` entry (dict order = README order). Adding a size: append to `SIZES` (kept in descending order).
- Regeneration is deterministic: with unchanged sources and pinned dependencies, output PNGs are byte-identical run-to-run. A dirty `output/` diff after a run therefore always means a real change.
- `requirements.txt` is a full pinned freeze (direct deps: `CairoSVG`, `pillow`; the rest are transitive). Updates rely on **GitHub security alerts only — there is no scheduled Dependabot config** in this repo (no `.github/dependabot.yml`), so routine version bumps are manual. If you want scheduled updates, add a `pip`/weekly `.github/dependabot.yml` and update this line. Note that a Pillow major upgrade can change resize interpolation and hence PNG bytes — regenerate and eyeball a couple of sizes when bumping it.
