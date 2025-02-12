from flask import Flask, render_template, request, Blueprint
import os
import base64
import random

app = Flask(__name__)
IGBP = Blueprint("IGBP", __name__)

# Define the path to the Character_Desgin folder
CHARACTER_DESIGN_DIR = os.path.join(os.getcwd(), "Character_Desgin")
CHARACTER_POSES_DIR = os.path.join(os.getcwd(), "Character_pose")
CHARACTER_EXPRESSION_DIR = os.path.join(os.getcwd(), "Character_Expression")

def get_images():
    """Reads images from the folder and encodes them in base64 for direct embedding."""
    images = []
    if os.path.exists(CHARACTER_DESIGN_DIR):
        for filename in os.listdir(CHARACTER_DESIGN_DIR):
            if filename.lower().endswith(('png', 'jpg', 'jpeg', 'gif')):
                filepath = os.path.join(CHARACTER_DESIGN_DIR, filename)
                with open(filepath, "rb") as image_file:
                    encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
                    images.append(f"data:image/{filename.split('.')[-1]};base64,{encoded_image}")
    if images:
        Random = random.choice(images)
        return Random
    else:
        return None

@IGBP.route("/generate_desgin", methods=["GET", "POST"])
def generate_design():
    image = None
    if request.method == "POST":
        image = get_images()  # Fetch images when button is clicked
    return render_template("image_generation.html", image=image)

if __name__ == "__main__":
    app.run(debug=True)
