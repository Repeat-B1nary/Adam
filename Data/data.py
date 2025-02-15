import json
import os

def write_data(data, storage):
    # If file doesn't exist, create an empty list
    if not os.path.exists(storage):
        users = []
    else:
        with open(storage, 'r') as f:
            try:
                users = json.load(f)
                if not isinstance(users, list):  # Ensure it's a list
                    users = []
            except json.JSONDecodeError:
                users = []  # Handle broken JSON

    # Append new user
    users.append(data)

    # Write back to file with correct format
    with open(storage, 'w') as f:
        json.dump(users, f, indent=4)

    print("Data saved to data.json")
    return True

    
import json

def read_data(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)  # Load JSON file
            if not isinstance(data, list):
                raise ValueError("Invalid user data format: Expected a list of users")
            return data
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"❌ Error loading data: {e}")
        return []  # Return an empty list if there's an error
