from flask import Flask,render_template
import name_randomizer
import os
import requests
import re
import random

if 'static' not in os.listdir():
    os.mkdir('static')

PEOPLE_FOLDER ='static'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER

@app.route('/')
@app.route('/index')
def place_holder():
    image= os.path.join(app.config['UPLOAD_FOLDER'],'image.jpg')
    ids=name_randomizer.identity().info
    return render_template("index.html", user_image=image,id_s=ids)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port='8888')
