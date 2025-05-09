import cairosvg
from PIL import Image

base_content = open('assets/base.svg').read()
background_content = open('assets/background.svg').read()
dumbbell_content = open('assets/dumbbell.svg').read()

colors = {
    'gradient': 'url(#bgGradient)',
    'dark': '#383838',
    'transparent': '',
}

variants = {
    'full_gradient': {
        'background': True,
        'background_color': 'gradient',
        'dumbbell': True,
        'dumbbell_color': 'dark',
    },
    'full_dark': {
        'background': True,
        'background_color': 'dark',
        'dumbbell': True,
        'dumbbell_color': 'gradient',
    },
    'dumbbell_gradient': {
        'background': False,
        'background_color': 'transparent',
        'dumbbell': True,
        'dumbbell_color': 'gradient',
    },
    'dumbbell_dark': {
        'background': False,
        'background_color': 'transparent',
        'dumbbell': True,
        'dumbbell_color': 'dark',
    }
}

sizes = [
    1600,
    1024,
    512,
    400,
    300,
    180,
    120,
    60,
    30,
    16,
]

readme_str = ''
generated_files_list = []

for variant in variants:
    data = variants[variant]
    content = base_content

    if data['background']:
        content = content.replace('<!-- Background -->', background_content)
        content = content.replace('{background_color}', colors[data['background_color']])

    if data['dumbbell']:
        content = content.replace('<!-- Dumbbell -->', dumbbell_content)
        content = content.replace('{dumbbell_color}', colors[data['dumbbell_color']])
    
    f = open(f'output/{variant}.svg', 'w')
    f.write(content)
    f.close()
    generated_files_list.append(f'{variant}.svg')

    cairosvg.svg2png(url=f'output/{variant}.svg', write_to=f'output/{variant}.png')
    generated_files_list.append(f'{variant}.png')

    readme_str += f'### {variant}\n'
    readme_str += f'![{variant.title()} Logo](output/{variant}.png)\n\n'

    with Image.open(f'output/{variant}.png') as img:
        for size in sizes:
            size_str = str(size) + 'x' + str(size)
            img_resized = img.resize((size, size))
            img_resized.save(f'output/{variant}_{size_str}.png')
            generated_files_list.append(f'{variant}_{size_str}.png')

with open('README.md', 'r') as readme_file:
    readme_content = readme_file.read()

readme_content = readme_content.split('## Variants')[0] + '## Variants\n\n' + readme_str

readme_content += '## Generated Files\n\n'
for g in generated_files_list:
    readme_content += f'- [{g}](output/{g})\n'

with open('README.md', 'w') as readme_file:
    readme_file.write(readme_content)
