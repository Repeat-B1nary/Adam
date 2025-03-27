import os
from flask import Flask, redirect, session, url_for, render_template, request
from Generate.image_generation import IGBP
from Auth.signup import signup_bp
from Auth.login import login_bp
from Data.data import read_data
from pathlib import Path

app = Flask(__name__)
app.config['SECRET_KEY'] = 'KingVon'


app.register_blueprint(IGBP)
app.register_blueprint(signup_bp)
app.register_blueprint(login_bp)


UPLOAD_FOLDER = "User_Uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/profile')
def profile():
    if "user_id" not in session:
        return redirect(url_for("login.login")) 

    user_id = session["user_id"]  
    user_info = read_data('user_info.json')

    
    user = next((u for u in user_info if u['user_id'] == user_id), None)

    if not user:
        return redirect(url_for("login.login"))  

    username = user['username']
    password = user['password']
    email = user['email']
    gender = user['gender']
    dob = user['dob']
    
    
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
        return redirect(url_for("login.login")) 

    user_id = session['user_id'] 
    folder = []

    current_file_path = Path(__file__)
    parent_directory = current_file_path.parents[0]
    users_folder = os.path.join(parent_directory, 'User_Uploads', user_id)
    print("user folder: " + users_folder)

    if os.path.exists(users_folder):
        users_created_folder = os.listdir(users_folder)
        folder.extend(users_created_folder)

    print("folder: "+ str(folder))


    if request.method == 'POST':
        # Handling Image Upload
        if 'image' in request.files:
            image = request.files['image']
            folder_name = request.form.get("folder_name")

            image_path = os.path.join(users_folder, folder_name, image.filename)
            image.save(image_path)

            return redirect(url_for("IGBP.generate_design"))

        # Handling Folder Creation
        elif 'create_folder' in request.form:
            folder_name = request.form.get("folder_name")
            user_folder_create = os.path.join(users_folder, folder_name)
            os.makedirs(user_folder_create, exist_ok=True)

            return redirect(url_for("IGBP.generate_design"))

    return render_template("upload.html", folder=folder)



@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login.login'))

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/about/Privacy_Policy')
def Privacy_Policy():
    return render_template("Privacy_Policy.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5035))
    app.run(host="0.0.0.0", port=port, debug=True)
