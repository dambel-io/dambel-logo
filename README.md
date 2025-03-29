# Dambel - Logo
This is the initial version of the **Dambel** logo.

It may seem unusual, but it was designed using **HTML and CSS** to keep it super minimalistic and simple. You can extract the image by simply taking a screenshot of the specific `<div>` element in the browser.

## Code Usage

To work with and generate different sizes of the Dambel logo, follow these steps:

1. **Edit the Logo Design**:
   - Open [`logo.html`](logo.html) and modify the design of the logo if needed.

2. **Take the Screenshot**:
   - Open the `logo.html` file in your browser.
   - Capture a screenshot only from the logo division (make sure you capture just the logo and not the entire page).
   
3. **Enable/Disable Border (Optional)**:
   - You can enable or disable the box border as per your design preference by adjusting the code in `logo.html`.

4. **Save the Screenshot**:
   - After capturing the screenshot, paste the image into [`files/main.png`](files/main.png) (make sure the image is named `main.png`).

5. **Install Pillow Library**:
   - Ensure you have the Python Pillow library installed. If you don't have it, install it by running:
     ```bash
     pip3 install pillow
     ```

6. **Generate Different Sizes**:
   - Run the script to automatically generate all the necessary logo sizes:
     ```bash
     python3 generate_sizes.py
     ```

7. **Generated Images**:
   - The generated images will be saved into the [`files/`](files/) directory.

8. **Auto-Generated Images List**:
   - The list of images below is automatically generated by the script when you run it.

## Images

### 1600x1600
The biggest version available

![Main Dambel Logo](files/1600x1600.png)

### 1024x1024
High resolution for website headers, print, or large displays

![Main Dambel Logo](files/1024x1024.png)

### 512x512
For use in favicons and app stores (e.g., Apple App Store, Google Play Store)

![Main Dambel Logo](files/512x512.png)

### 400x400
Medium size for social media profile images (Facebook, Twitter, etc.)

![Main Dambel Logo](files/400x400.png)

### 300x300
Medium-sized logo for email signatures or smaller sections of website

![Main Dambel Logo](files/300x300.png)

### 180x180
Icons for mobile apps or small website icons

![Main Dambel Logo](files/180x180.png)

### 120x120
Smaller app icons (used on mobile or desktop apps)

![Main Dambel Logo](files/120x120.png)

### 60x60
Favicons or small logo images on social media profiles

![Main Dambel Logo](files/60x60.png)

### 30x30
Very small logo for favicon, small icons, or toolbar logos

![Main Dambel Logo](files/30x30.png)

