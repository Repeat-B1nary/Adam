from flask import Flask, render_template, request, Blueprint, url_for, session, redirect
import os
import base64
import random

app = Flask(__name__)
IGBP = Blueprint("IGBP", __name__)

# Base directory where all user uploads are stored
USER_UPLOADS_DIR = os.path.join(os.getcwd(), "User_Uploads")

def get_images(directory):
    """Reads images from the given folder and encodes them in base64 for direct embedding."""
    images = []
    if os.path.exists(directory):
        for filename in os.listdir(directory):
            if filename.lower().endswith(('png', 'jpg', 'jpeg', 'gif')):
                filepath = os.path.join(directory, filename)
                with open(filepath, "rb") as image_file:
                    encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
                    images.append(f"data:image/{filename.split('.')[-1]};base64,{encoded_image}")
    
    return random.choice(images) if images else None

@IGBP.route("/generate_desgin", methods=["GET", "POST"])
def generate_design():
    if 'user_id' not in session:
        return redirect(url_for('login.login'))
    
    user_id = session['user_id']  # Retrieve user_id from session
    user_folder = os.path.join(USER_UPLOADS_DIR, str(user_id))  # Path to user's folder

    # Define user-specific paths
    character_design_dir = os.path.join(user_folder, "Character_Desgin")
    character_poses_dir = os.path.join(user_folder, "Character_pose")
    character_expression_dir = os.path.join(user_folder, "Character_Expression")

    images = []
    
    if request.method == "POST":
        selection = request.form.getlist("selection")
        print("Selection: ", selection)

        for item in selection:
            if item == "Character Design":
                image = get_images(character_design_dir)
            elif item == "Character Pose":
                image = get_images(character_poses_dir)
            elif item == "Character Expression":
                image = get_images(character_expression_dir)
            else:
                image = None

            if image:
                images.append(image)

    return render_template("image_generation.html", images=images)

if __name__ == "__main__":
    app.run(debug=True)
