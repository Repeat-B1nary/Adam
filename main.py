import os
from flask import Flask, redirect, session, url_for, render_template, request
from Generate.image_generation import IGBP
from Auth.signup import signup_bp
from Auth.login import login_bp
from Data.data import read_data

app = Flask(__name__)
app.config['SECRET_KEY'] = 'KingVon'

# Register Blueprints
app.register_blueprint(IGBP)
app.register_blueprint(signup_bp)
app.register_blueprint(login_bp)

# Define directories
UPLOAD_FOLDER = "User_Uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/profile')
def profile():
    if "user_id" not in session:
        return redirect(url_for("login.login"))  # Redirect to login if not authenticated

    user_id = session["user_id"]  # Get logged-in user's ID
    user_info = read_data('user_info.json')

    # Find the user's info
    user = next((u for u in user_info if u['user_id'] == user_id), None)

    if not user:
        return redirect(url_for("login.login"))  # If user not found, re-login

    username = user['username']
    password = user['password']
    email = user['email']
    gender = user['gender']
    dob = user['dob']
    
    # Locate the profile picture
    user_folder = os.path.join("static", "profile_pics", user_id)
    profile_pic = None

    if os.path.exists(user_folder):
        files = os.listdir(user_folder)
        if files:
            profile_pic = f"profile_pics/{user_id}/{files[0]}"
            print(f"Profile Picture Path: {profile_pic}")


    return render_template('profile.html', username=username, password=password, email=email, gender=gender, dob=dob, profile_pic=profile_pic)

@app.route("/")
def home():

    return render_template("home.html")


@app.route("/upload", methods=["POST", "GET"])
def index():
    if "user_id" not in session:
        return redirect(url_for("login.login"))  # Redirect to login if not authenticated


    if request.method == "POST":
        type = request.form.get("type")
        image = request.files.get("image")

        user_id = session["user_id"]  # Get logged-in user's ID
        user_folder = os.path.join(app.config['UPLOAD_FOLDER'], user_id, type)  # Unique folder for user

        if not os.path.exists(user_folder):
            os.makedirs(user_folder)  # Create user-specific folder if it doesn't exist

        if image:
            # Save image in the user's specific folder
            image_path = os.path.join(user_folder, image.filename)
            image.save(image_path)

            return render_template("upload.html", image_path=image_path)

    return render_template("upload.html", image_path=None)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login.login'))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5035))
    app.run(host="0.0.0.0", port=port, debug=True)
