from flask import Flask, render_template, request, Blueprint, url_for, session, redirect
from pathlib import Path
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

@IGBP.route("/generate_design", methods=["GET", "POST"])
def generate_design():
    if 'user_id' not in session:
        return redirect(url_for('login.login'))
    
    user_id = session['user_id']
    folders = []
    images_pulled = []
    image = None  

    current_file_path = Path(__file__)
    parent_directory = current_file_path.parents[1]
    users_folder = os.path.join(parent_directory, 'User_Uploads', user_id)

    if os.path.exists(users_folder):
        users_created_folder = os.listdir(users_folder)
        folders.extend(users_created_folder)

    if request.method == "POST":
        folder_name = request.form.getlist("folder_name")  
        print("folder name: "+ str(folder_name))  

        for folder_names in folder_name:
            folder_path = os.path.join(parent_directory, 'User_Uploads', user_id, folder_names)
            image = get_images(folder_path)
            if image:  
                images_pulled.append(image)
            
            


    return render_template("image_generation.html", users_folder=users_folder, folders=folders, images_pulled=images_pulled)


if __name__ == "__main__":
    app.run(debug=True)
