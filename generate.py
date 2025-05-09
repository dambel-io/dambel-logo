from PIL import Image

variants = ['full']
formats = ['png']
sizes = [
    [1600, 'The biggest version available'],
    [1024, 'High resolution for website headers, print, or large displays'],
    [512, 'For use in app stores (e.g., Apple App Store, Google Play Store)'],
    [400, 'Medium size for social media profile images (Facebook, Twitter, etc.)'],
    [300, 'Medium-sized logo for email signatures or smaller sections of website'],
    [180, 'Icons for mobile apps or small website icons'],
    [120, 'Smaller app icons (used on mobile or desktop apps)'],
    [60, 'Favicons or small logo images on social media profiles'],
    [30, 'Very small logo for favicon, small icons, or toolbar logos'],
    [16, 'Best for favicon'],
]

readme_str = ''

with Image.open('files/main.png') as img:
    for variant in variants:
        for format in formats:
            for size in sizes:
                size_str = str(size[0]) + 'x' + str(size[0])
                img_resized = img.resize((size[0], size[0]))
                fname = f'{variant}_{size_str}.{format}'
                img_resized.save(f'files/{fname}')

                readme_str += f'### {fname}\n'
                readme_str += f'{size[1]}\n\n'
                readme_str += f'![{variant.title()} Logo](files/{fname})\n\n'

with open('README.md', 'r') as readme_file:
    readme_content = readme_file.read()

readme_content = readme_content.split('## Images')[0] + '## Images\n\n' + readme_str

with open('README.md', 'w') as readme_file:
    readme_file.write(readme_content)
