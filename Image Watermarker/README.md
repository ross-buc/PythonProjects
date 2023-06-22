# Image WaterMarker

A Python project that utilizes Tkinter and Pillow libraries to add watermarks to image files and save them to a specified directory.

## Features

- Allows the user to select an image file and display it in a Tkinter window.
- Resizes the image to fit the Tkinter window while maintaining aspect ratio.
- Adds a watermark to the image using a predefined watermark image.
- Saves the watermarked image to the specified directory.
- Provides options to save and reset the watermarked image.

## Prerequisites

- Python 3.x
- Tkinter library
- Pillow library

## Usage

1. Clone the repository or download the source code.

2. Install the required dependencies:

   ```bash
   pip install pillow
3. Run the script 
   ```bash
   python main.py
4. Click the "Add Photo" button to select an image file.

5. The selected image will be displayed in the Tkinter window.

6. The image will be resized to fit the window while maintaining the aspect ratio.

7. A watermark will be added to the image.

8. Click the "Save Image" button to save the watermarked image to the specified directory.

9. Click the "Reset" button to remove the current image and reset the window.

## Customization

- Change the directory variable in the code to specify the directory where the watermarked images should be saved.

- Adjust the watermark_size variable to set the desired size of the watermark.

## Supported Image Formats

The application supports the following image formats:

- JPEG (.jpg, .jpeg)
- PNG (.png)
- GIF (.gif)
- BMP (.bmp)
