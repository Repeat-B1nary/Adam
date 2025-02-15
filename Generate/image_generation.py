from flask import Flask, render_template, request, Blueprint, url_for, session, redirect
import os
import base64
import random

app = Flask(__name__)
IGBP = Blueprint("IGBP", __name__)

# Define the path to the Character_Desgin folder
CHARACTER_DESIGN_DIR = os.path.join(os.getcwd(), "Character_Desgin")
CHARACTER_POSES_DIR = os.path.join(os.getcwd(), "Character_pose")
CHARACTER_EXPRESSION_DIR = os.path.join(os.getcwd(), "Character_Expression")

def get_images(Dir):
    """Reads images from the folder and encodes them in base64 for direct embedding."""
    images = []
    if os.path.exists(Dir):
        for filename in os.listdir(Dir):
            if filename.lower().endswith(('png', 'jpg', 'jpeg', 'gif')):
                filepath = os.path.join(Dir, filename)
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
    if 'user_id' not in session:
        return redirect(url_for('login.login'))
    
    images = []
    if request.method == "POST":
        selection = request.form.getlist("selection")
        print("selection: ",selection)

        for selection in selection:
            print("selection: ",selection)
            if selection == "Character Design":
                image = get_images(CHARACTER_DESIGN_DIR)  # Fetch images when button i
                if image:
                    images.append(image)
                else:
                    None
            elif selection == "Character Pose":
                image = get_images(CHARACTER_POSES_DIR)
                if image:
                    images.append(image)
                else:
                    None
            elif selection == "Character Expression":
                image = get_images(CHARACTER_EXPRESSION_DIR)
                if image:
                    images.append(image)
                else:
                    None

    return render_template("image_generation.html", images=images)

if __name__ == "__main__":
    app.run(debug=True)