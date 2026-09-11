"""Generate all Dambel logo variants (SVG + PNG in every size) from the assets/ fragments.

Each variant is assembled by splicing SVG fragments into a base template
(text substitution of the `<!-- Background -->` / `<!-- Dumbbell -->` placeholders
and the `{background_color}` / `{dumbbell_color}` tokens), rendered to a full-size
PNG with CairoSVG, then resized to every entry in SIZES with Pillow.
The variant list at the bottom of README.md is regenerated on every run.
"""

from dataclasses import dataclass
from pathlib import Path

import cairosvg
from PIL import Image

ASSETS_DIR = Path('assets')
OUTPUT_DIR = Path('output')
README = Path('README.md')

# Marker in README.md below which the variant list is regenerated.
README_MARKER = '## Variants'

COLORS = {
    'gradient': 'url(#bgGradient)',  # defined in the base templates' <defs>
    'dark': '#383838',
    'white': '#ffffff',
}


@dataclass(frozen=True)
class Variant:
    background: str | None  # asset fragment name ('background' | 'rounded' | 'circle') or None for transparent
    background_color: str | None  # key into COLORS, None when there is no background
    dumbbell_color: str  # key into COLORS
    tight: bool = False  # use the cropped (tight) base template and dumbbell fragment
    animated: bool = False  # use the pumping dumbbell_loader fragment; SVG-only, no PNG size set


VARIANTS = {
    'full_gradient': Variant('background', 'gradient', 'dark'),
    'full_gradient_white': Variant('background', 'gradient', 'white'),
    'full_dark': Variant('background', 'dark', 'gradient'),
    'full_dark_white': Variant('background', 'dark', 'white'),
    'rounded_gradient': Variant('rounded', 'gradient', 'dark'),
    'rounded_gradient_white': Variant('rounded', 'gradient', 'white'),
    'rounded_dark': Variant('rounded', 'dark', 'gradient'),
    'rounded_dark_white': Variant('rounded', 'dark', 'white'),
    'dumbbell_gradient': Variant(None, None, 'gradient'),
    'dumbbell_dark': Variant(None, None, 'dark'),
    'dumbbell_white': Variant(None, None, 'white'),
    'dumbbell_gradient_tight': Variant(None, None, 'gradient', tight=True),
    'dumbbell_dark_tight': Variant(None, None, 'dark', tight=True),
    'dumbbell_white_tight': Variant(None, None, 'white', tight=True),
    'circle_gradient': Variant('circle', 'gradient', 'dark'),
    'circle_gradient_white': Variant('circle', 'gradient', 'white'),
    'circle_dark': Variant('circle', 'dark', 'gradient'),
    'circle_dark_white': Variant('circle', 'dark', 'white'),
}

# Every variant above also gets an animated `_loader` sibling: same background/colors,
# but the dumbbell mark pumps (see dumbbell_loader.svg). SVG-only — a PNG can't animate.
VARIANTS = {
    variant_name: variant
    for name, base_variant in list(VARIANTS.items())
    for variant_name, variant in (
        (name, base_variant),
        (f'{name}_loader', Variant(base_variant.background, base_variant.background_color,
                                    base_variant.dumbbell_color, tight=base_variant.tight, animated=True)),
    )
}

SIZES = [1600, 1024, 512, 400, 300, 192, 180, 144, 120, 96, 72, 60, 48, 30, 16]

FRAGMENT_NAMES = [
    'base', 'base_tight',
    'background', 'rounded', 'circle',
    'dumbbell', 'dumbbell_tight', 'dumbbell_loader',
]


def load_fragments() -> dict[str, str]:
    return {name: (ASSETS_DIR / f'{name}.svg').read_text() for name in FRAGMENT_NAMES}


def assemble_svg(variant: Variant, fragments: dict[str, str]) -> str:
    content = fragments['base_tight' if variant.tight else 'base']
    if variant.background:
        content = content.replace('<!-- Background -->', fragments[variant.background])
        content = content.replace('{background_color}', COLORS[variant.background_color])
    if variant.animated:
        dumbbell_fragment = 'dumbbell_loader'
    else:
        dumbbell_fragment = 'dumbbell_tight' if variant.tight else 'dumbbell'
    content = content.replace('<!-- Dumbbell -->', fragments[dumbbell_fragment])
    content = content.replace('{dumbbell_color}', COLORS[variant.dumbbell_color])
    return content


def render_variant(name: str, variant: Variant, fragments: dict[str, str]) -> list[str]:
    """Write the variant's SVG and PNGs to OUTPUT_DIR; return the generated file names."""
    svg_path = OUTPUT_DIR / f'{name}.svg'
    svg_path.write_text(assemble_svg(variant, fragments))
    generated = [svg_path.name]

    if variant.animated:
        # SVG-only — a PNG can only capture one frozen frame of the pump animation.
        png_path = OUTPUT_DIR / f'{name}.png'
        if png_path.exists():
            png_path.unlink()
        return generated

    png_path = OUTPUT_DIR / f'{name}.png'
    cairosvg.svg2png(url=str(svg_path), write_to=str(png_path))
    generated.append(png_path.name)

    with Image.open(png_path) as img:
        for size in SIZES:
            resized_path = OUTPUT_DIR / f'{name}_{size}x{size}.png'
            img.resize((size, size), Image.Resampling.BICUBIC).save(resized_path)
            generated.append(resized_path.name)
    return generated


def readme_section(name: str, variant: Variant, generated: list[str]) -> str:
    section = f'\n### {name}\n'
    if variant.animated:
        section += '_Animated (pumping dumbbell) — open the SVG to see it move._\n'
        section += f'<img src="output/{name}.svg" style="width: 50%" />\n\n'
    else:
        section += f'<img src="output/{name}.png" style="width: 50%" />\n\n'
    for file_name in generated:
        section += f'- [{file_name}](output/{file_name})\n'
    return section


def update_readme(sections: str) -> None:
    head = README.read_text().split(README_MARKER)[0]
    README.write_text(head + README_MARKER + '\n\n' + sections)


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    fragments = load_fragments()
    sections = ''
    for name, variant in VARIANTS.items():
        generated = render_variant(name, variant, fragments)
        sections += readme_section(name, variant, generated)
    update_readme(sections)


if __name__ == '__main__':
    main()
