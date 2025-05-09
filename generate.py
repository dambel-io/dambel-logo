from PIL import Image

needed_sizes = [
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
    for needed_size in needed_sizes:
        size = needed_size[0]
        img_resized = img.resize((size, size))
        size_str = str(size) + 'x' + str(size)
        
        img_resized.save(f'files/{size_str}.png')

        readme_str += f'### {size_str}\n'
        readme_str += f'{needed_size[1]}\n\n'
        readme_str += f'![Main Dambel Logo](files/{size_str}.png)\n\n'

with open('README.md', 'r') as readme_file:
    readme_content = readme_file.read()

readme_content = readme_content.split('## Images')[0] + '## Images\n\n' + readme_str

with open('README.md', 'w') as readme_file:
    readme_file.write(readme_content)
