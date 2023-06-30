"""
This is a Flask-based web application that allows users to upload an image and get the top 10 dominant colors in that image.
"""
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
from PIL import Image
import os
import numpy as np

app = Flask(__name__)
app.config["SECRET_KEY"] = "SECRET KEY"
app.config[
    "UPLOAD_FOLDER"
] = r"C:\Users\Buchanan\Documents\VSC\day-91\static\images"  # Choose your upload directory
Bootstrap(app)


def rgb_to_hex(colors):
    hex_color = []
    for color in colors:
        hex = "#{:02x}{:02x}{:02x}".format(color[0], color[1], color[2])
        hex_color.append(hex)
    return hex_color


def color_percentage(total_pixels, counts):
    percentage_list = []
    for count in counts:
        percentage_list.append(round(count / total_pixels * 100, 4))
    return percentage_list


def top_colors(file_path):
    with Image.open(file_path).convert("RGB") as img:
        # Resize the image
        baseheight = 500
        hpercent = baseheight / img.size[1]
        wsize = int(img.size[0] * hpercent)
        img = img.resize((wsize, baseheight), Image.ANTIALIAS)

        # Make into Numpy array
        na = np.array(img)
        delta = 24  # For example
        rounded_na = (
            np.round(na / delta) * delta
        )  # This rounds each color component to the nearest multiple of delta
        rounded_na = rounded_na.astype(int)  # Convert to integer

        total_pixels = rounded_na.size // 3
        # Arrange all pixels into a tall column of 3 RGB values and find unique rows (colours)
        colours, counts = np.unique(rounded_na.reshape(-1, 3), axis=0, return_counts=1)

        # Sort colours based on counts
        sorted_indices = np.argsort(counts)[::-1]
        sorted_colours = colours[sorted_indices]
        sorted_counts = counts[sorted_indices]

        # Get top 10
        top_10_colors = sorted_colours[:10]
        top_10_counts = sorted_counts[:10]

        # Convert RGB to HEX Code
        hexed_colors = rgb_to_hex(top_10_colors)

        # Convert counts to percentage
        percentage_list = color_percentage(total_pixels, top_10_counts)

        color_dict = {}
        for _ in range(len(hexed_colors)):
            color_dict[hexed_colors[_]] = percentage_list[_]

    return color_dict


@app.route("/")
def home():
    image = None
    return render_template("index.html", image=image, img_color=None)


@app.route("/upload", methods=("GET", "POST"))
def upload():
    if "imageFile" in request.files:
        file = request.files["imageFile"]
        if file.filename != "":
            file_name = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], file_name))
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], file_name)
            print(file_path)
            index = file_path.find("static")
            new_file_path = file_path[index:]
            color_dict = top_colors(file_path)
            return render_template(
                "index.html", image=new_file_path, color_dict=color_dict
            )
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
