import cairosvg
from PIL import Image

base_content = open('assets/base.svg').read()
base_tight_content = open('assets/base_tight.svg').read()
background_content = open('assets/background.svg').read()
rounded_content = open('assets/rounded.svg').read()
circle_background_content = open('assets/circle.svg').read()
dumbbell_content = open('assets/dumbbell.svg').read()
dumbbell_tight_content = open('assets/dumbbell_tight.svg').read()

colors = {
    'gradient': 'url(#bgGradient)',
    'dark': '#383838',
    'white': '#ffffff',
    'transparent': '',
}

variants = {
    'full_gradient': {
        'background': True,
        'background_color': 'gradient',
        'dumbbell': True,
        'dumbbell_color': 'dark',
        'circle': False,
    },
    'full_gradient_white': {
        'background': True,
        'background_color': 'gradient',
        'dumbbell': True,
        'dumbbell_color': 'white',
        'circle': False,
    },
    'full_dark': {
        'background': True,
        'background_color': 'dark',
        'dumbbell': True,
        'dumbbell_color': 'gradient',
        'circle': False,
    },
    'full_dark_white': {
        'background': True,
        'background_color': 'dark',
        'dumbbell': True,
        'dumbbell_color': 'white',
        'circle': False,
    },
    'rounded_gradient': {
        'background': True,
        'background_color': 'gradient',
        'dumbbell': True,
        'dumbbell_color': 'dark',
        'circle': False,
        'rounded': True,
    },
    'rounded_gradient_white': {
        'background': True,
        'background_color': 'gradient',
        'dumbbell': True,
        'dumbbell_color': 'white',
        'circle': False,
        'rounded': True,
    },
    'rounded_dark': {
        'background': True,
        'background_color': 'dark',
        'dumbbell': True,
        'dumbbell_color': 'gradient',
        'circle': False,
        'rounded': True,
    },
    'rounded_dark_white': {
        'background': True,
        'background_color': 'dark',
        'dumbbell': True,
        'dumbbell_color': 'white',
        'circle': False,
        'rounded': True,
    },
    'dumbbell_gradient': {
        'background': False,
        'background_color': 'transparent',
        'dumbbell': True,
        'dumbbell_color': 'gradient',
        'circle': False,
    },
    'dumbbell_dark': {
        'background': False,
        'background_color': 'transparent',
        'dumbbell': True,
        'dumbbell_color': 'dark',
        'circle': False,
    },
    'dumbbell_white': {
        'background': False,
        'background_color': 'transparent',
        'dumbbell': True,
        'dumbbell_color': 'white',
        'circle': False,
    },
    'dumbbell_gradient_tight': {
        'background': False,
        'background_color': 'transparent',
        'dumbbell': True,
        'dumbbell_color': 'gradient',
        'circle': False,
        'tight': True,
    },
    'dumbbell_dark_tight': {
        'background': False,
        'background_color': 'transparent',
        'dumbbell': True,
        'dumbbell_color': 'dark',
        'circle': False,
        'tight': True,
    },
    'dumbbell_white_tight': {
        'background': False,
        'background_color': 'transparent',
        'dumbbell': True,
        'dumbbell_color': 'white',
        'circle': False,
        'tight': True,
    },
    'circle_gradient': {
        'background': True,
        'background_color': 'gradient',
        'dumbbell': True,
        'dumbbell_color': 'dark',
        'circle': True,
    },
    'circle_gradient_white': {
        'background': True,
        'background_color': 'gradient',
        'dumbbell': True,
        'dumbbell_color': 'white',
        'circle': True,
    },
    'circle_dark': {
        'background': True,
        'background_color': 'dark',
        'dumbbell': True,
        'dumbbell_color': 'gradient',
        'circle': True,
    },
    'circle_dark_white': {
        'background': True,
        'background_color': 'dark',
        'dumbbell': True,
        'dumbbell_color': 'white',
        'circle': True,
    },
}

sizes = [
    1600,
    1024,
    512,
    400,
    300,
    192,
    180,
    144,
    120,
    96,
    72,
    60,
    48,
    30,
    16,
]

readme_str = ''

for variant in variants:
    generated_files_list = []
    data = variants[variant]
    is_tight = data.get('tight', False)
    content = base_tight_content if is_tight else base_content

    if data['background']:
        if data['circle']:
            bg = circle_background_content
        elif data.get('rounded'):
            bg = rounded_content
        else:
            bg = background_content
        content = content.replace('<!-- Background -->', bg)
        content = content.replace('{background_color}', colors[data['background_color']])

    if data['dumbbell']:
        db_content = dumbbell_tight_content if is_tight else dumbbell_content
        content = content.replace('<!-- Dumbbell -->', db_content)
        content = content.replace('{dumbbell_color}', colors[data['dumbbell_color']])

    f = open(f'output/{variant}.svg', 'w')
    f.write(content)
    f.close()
    generated_files_list.append(f'{variant}.svg')

    cairosvg.svg2png(url=f'output/{variant}.svg', write_to=f'output/{variant}.png')
    generated_files_list.append(f'{variant}.png')

    readme_str += f'\n### {variant}\n'
    readme_str += f'<img src="output/{variant}.png" style="width: 50%" />\n\n'

    with Image.open(f'output/{variant}.png') as img:
        for size in sizes:
            size_str = str(size) + 'x' + str(size)
            img_resized = img.resize((size, size))
            img_resized.save(f'output/{variant}_{size_str}.png')
            generated_files_list.append(f'{variant}_{size_str}.png')

    for g in generated_files_list:
        readme_str += f'- [{g}](output/{g})\n'

with open('README.md', 'r') as readme_file:
    readme_content = readme_file.read()

readme_content = readme_content.split('## Variants')[0] + '## Variants\n\n' + readme_str

with open('README.md', 'w') as readme_file:
    readme_file.write(readme_content)
