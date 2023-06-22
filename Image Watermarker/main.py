"""
A python project using Tkinter and Pillow to watermark image files and save them to the directory
"""
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import os


class ImageWaterMarkerApp:
    def __init__(self):
        self.directory = "C:/Users/Pictures/Watermark/"  # Change path to where you want the image saved
        self.watermark_size = (25, 25)  # Adjust the size as desired
        self.filename = None
        self.imaged = None
        self.window = Tk()
        self.window.geometry("1250x1000")
        self.window.title("Image WaterMarker")

        # Create a button to add an image
        ttk.Button(text="Add Photo", command=self.upload_action).pack()

        # Create a label to display the image
        self.image_label = ttk.Label(self.window)
        self.image_label.pack()

        # Create the Save button (initially hidden)
        self.save_button = ttk.Button(text="Save Image", command=self.save_image)

        # Create the Reset button (initially hidden)
        self.reset_button = ttk.Button(text="Reset", command=self.reset_action)

        self.window.mainloop()

    def save_image(self):
        """
        Saving the completed image
        """
        original_file_name = os.path.basename(self.filename)
        remove_ext = os.path.splitext(original_file_name)[0]
        new_file_name = f"{remove_ext}_watermarked.jpg"
        save_path = os.path.join(self.directory, new_file_name)
        self.imaged.save(save_path)
        print(f"Image saved as: {save_path}")

    def calculate_resized_dimensions(self, image, max_width, max_height):
        """
        Takes the selected image and resizes it to fit the Tkinter window

        Args:
            image : the selected image file
            max_width (_type_): Tkinter window width
            max_height (_type_): Tkinter window height

        Returns:
            The width and height suitable for the Tkinter window
        """
        width, height = image.size
        aspect_ratio = width / height
        if width > max_width or height > max_height:
            if width / max_width > height / max_height:
                width = max_width
                height = int(width / aspect_ratio)
            else:
                height = max_height
                width = int(height * aspect_ratio)
        return width, height

    def upload_action(self):
        """
        Opens your file directory and allows you search for an appropriate image file and displays it in the Tkinter window

        """
        f_types = [
            ("Image Files", ("*.jpg", "*.jpeg", "*.png", "*.gif", "*.bmp")),
            ("JPG Files", "*.jpg"),
            ("JPEG Files", "*.jpeg"),
            ("PNG Files", "*.png"),
            ("GIF Files", "*.gif"),
            ("BMP Files", "*.bmp"),
        ]
        self.filename = filedialog.askopenfilename(filetypes=f_types)
        if not self.filename:
            return  # If the user doesnt select a photo

        img = Image.open(self.filename)
        watermark = Image.open("watermark.png")
        watermark = watermark.resize(self.watermark_size)

        window_width = self.window.winfo_width()
        window_height = self.window.winfo_height()
        max_width = window_width - 20
        max_height = window_height - 20
        resized_width, resized_height = self.calculate_resized_dimensions(
            img, max_width, max_height
        )

        img_resized = img.resize((resized_width, resized_height))

        self.imaged = img_resized
        watermark_width, watermark_height = watermark.size
        x = self.imaged.width - watermark_width - 10
        y = self.imaged.height - watermark_height - 10
        self.imaged.paste(watermark, (x, y), watermark)
        img_tk = ImageTk.PhotoImage(self.imaged)
        self.image_label.config(image=img_tk)
        self.image_label.image = img_tk

        self.save_button.pack()  # Show the Save button
        self.reset_button.pack()  # Show the Reset button

    def reset_action(self):
        """
        Removes the current image and resets the window back to the original state
        """
        self.image_label.config(image=None)
        self.image_label.image = None
        self.save_button.pack_forget()  # Hide the save button if there is no image displayed
        self.reset_button.pack_forget()  # Hide the resest button if there is no image displayed


if __name__ == "__main__":
    ImageWaterMarkerApp()
