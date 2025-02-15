from flask import Flask, Blueprint, request, render_template, redirect, url_for, session
from Validation.validation import SignupSchema
from Data.data import write_data
import string
import random
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # Set max file size (16MB)

signup_bp = Blueprint("sign_up", __name__)

profile_pics_storage = os.path.join("static", "profile_pics")
app.config["profile_pics_storage"] = profile_pics_storage

if not os.path.exists(profile_pics_storage):
    os.makedirs(profile_pics_storage, exist_ok=True)  
    print(f"Created directory: {os.path.abspath(profile_pics_storage)}")

def generate_userid():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(12))

@signup_bp.route("/sign-up", methods=['POST', 'GET'])
def sign_up():
    error = None

    try:
        if request.method == 'POST':
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '').strip()
            email = request.form.get('email', '').strip()
            dob = request.form.get('dob', '').strip()
            gender = request.form.get('gender', '').strip()
            user_id = generate_userid() 

            data = request.form.to_dict()
            data['user_id'] = user_id

            profile_pic = request.files.get("profile_pic")

            if profile_pic and profile_pic.filename:
                filename = secure_filename(profile_pic.filename)  # Ensure safe filename
                
                # Create a unique folder for the user
                user_folder = os.path.join(profile_pics_storage, user_id)
                os.makedirs(user_folder, exist_ok=True)  # Ensure directory exists
                
                # Create unique filename
                unique_filename = f"{user_id}_{filename}"  
                profile_pic_path = os.path.join(user_folder, unique_filename)

                try:
                    profile_pic.save(profile_pic_path)
                    print(f"✅ File saved at: {profile_pic_path}")
                    
                    # Store relative path in the database
                    data['profile_pic'] = os.path.join(user_id, unique_filename)
                except Exception as e:
                    print(f"❌ Error saving file: {e}")
                    data['profile_pic'] = None  # Default if file fails to save
            else:
                data['profile_pic'] = None

            print("sign_up: ", data)

            errors = SignupSchema().validate(data)
            if errors:
                error = {'validation_error': errors}
            else:
                write_data(data, 'user_info.json')
                return redirect(url_for('login.login'))
                
    except Exception as e:
        print(f"❌ An error occurred: {e}")

    return render_template('signup.html', error=error)


app.register_blueprint(signup_bp)

if __name__ == "__main__":
    app.run(debug=True)
