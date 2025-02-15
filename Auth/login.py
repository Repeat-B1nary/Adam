from flask import Blueprint, request, render_template, url_for, redirect, session
from Data.data import read_data
import json  # Ensuring JSON handling

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['POST', 'GET'])
def login():
    print("🔹 Route accessed: /login")  # Debug: Route hit

    error = None

    try:
        if request.method == 'POST':
            print("🔹 POST request received")  # Debug: POST request confirmed

            username = request.form.get('username')
            password = request.form.get('password')

            print(f"🔹 Form Data - Username: {username}, Password: {password}")  # Debug user input

            # Read stored user data
            try:
                users = read_data("user_info.json")  # Load user data
                print(f"🔹 Raw user data: {users}")  # Debug: Show full data

                # Ensure the data is a valid list
                if not isinstance(users, list):
                    raise ValueError("Invalid user data format: Expected a list of users")

                # Print each user for debugging
                for user in users:
                    print(f"🔹 Checking user: {user}")

                # Find user by username and password
                user = next((u for u in users if u["username"] == username and u["password"] == password), None)

                if user:
                    print(f"✅ User found: {user}")  # Debug: Show matched user
                    session['logged_in'] = True
                    session['user_id'] = user["user_id"]  # Store user_id in session
                    session['username'] = user["username"]  # Optional: Store username
                    return redirect(url_for('index'))
                else:
                    print("❌ Invalid username or password")  # Debug: No match found
                    error = 'Invalid username or password'

            except Exception as e:
                print(f"❌ Error reading user data: {e}")  # Debug: Show error details
                error = "An error occurred while retrieving user data."

    except Exception as err:
        print(f"❌ Login failed: {err}")  # Debug: Catch unexpected errors
        error = 'An error occurred. Please try again.'

    print(f"🔹 Rendering login page with error: {error}")  # Debug: Track errors
    return render_template('login.html', error=error)
