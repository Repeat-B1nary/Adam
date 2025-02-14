from flask import Flask
from flask import render_template, request
from Generate.image_generation import IGBP
import json
import os

app = Flask(__name__)

app.register_blueprint(IGBP)



Character_Desgin = 'Character_Desgin'
Character_Pose = "Character_Pose"
Character_Expression = "Character_Expression"

app.config['Character_Desgin'] = Character_Desgin
app.config['Character_Pose'] = Character_Pose
app.config['Character_Expression'] = Character_Expression



if not os.path.exists(Character_Desgin):
    os.makedirs(Character_Desgin)

if not os.path.exists(Character_Pose):
    os.makedirs(Character_Pose)
if not os.path.exists(Character_Expression):
    os.makedirs(Character_Expression)




@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == 'POST':
        type = request.form.get("type")
        print("type:" + type)
        image = request.files.get("image")
        print(image)
        if image:
            if type == "Character_Desgin":
                image_path = os.path.join(app.config['Character_Desgin'], image.filename)
                image.save(image_path)
                return render_template("index.html", image_path=image_path)
            elif type == "Character_Pose":
                image_path = os.path.join(app.config['Character_Pose'], image.filename)
                image.save(image_path)
                return render_template("index.html", image_path=image_path)
            else:
                image_path = os.path.join(app.config['Character_Expression'], image.filename)
                image.save(image_path)
                return render_template("index.html", image_path=image_path)
            

    
    return render_template("index.html", image_path=None)



if __name__ == "__main__":
    app.run(debug=True, port=5035)