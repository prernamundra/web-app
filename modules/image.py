#checked
from flask_restful import Resource
from flask import request,Response, render_template,flash,redirect,send_from_directory, abort, send_file,jsonify
import json
#-----------
from models import date
from models import userId
#-----------
from models import lognRes
from models import dbModel
from config.setup import app
#---------

from mysql.connector.utils import print_buffer
from werkzeug.utils import secure_filename
import os

from PIL import Image
from io import BytesIO

app.config["IMAGE_WORKER"] = "/home/ubuntu/integration/app/static/worker"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class AddImage(Resource):
    def post(self, worker_id):
        if request.method == "POST":
            if request.files:
                file_list = request.files.getlist("image[]")
                desc = request.form["desc"]
                desc = desc.strip().replace(" ","|")
                for image in file_list:
                    img = Image.open(BytesIO(image.read()))
                    w, h = img.size
                    img = img.resize((50+int(w/50), 50+int(h/50)),Image.ANTIALIAS)
                    if allowed_file(image.filename):
                        image_path = os.path.join(app.config["IMAGE_WORKER"], worker_id, "gallery")
                        if os.path.exists(image_path):
                            image_path = os.path.join(app.config["IMAGE_WORKER"], worker_id, "gallery")
                        else:
                            os.mkdir(image_path)
                    count = len(AddImage.filecounters(worker_id))+1
                    image_extension = 'webp'
                    profile_path = os.path.join(image_path, f"{worker_id}-{count}|{desc}.{image_extension}")
                    img.save(profile_path,optimize=True,quality=80)
                    
                flash("Photo upload","success")
                return redirect(f"/worker/profile")
            else:
                flash("Please try again !!","warning")
                return redirect(f"/worker/profile")

    def filecounters(worker_id):
        APP_FOLDER = "/home/ubuntu/integration/app/static/worker"
        imagepath = os.path.join(APP_FOLDER,worker_id,"gallery")
        workerpath = os.path.join(APP_FOLDER,worker_id)
        if os.path.exists(imagepath):
            pass
        else:  
            if os.path.exists(workerpath):
                pass
            else:
                os.mkdir(workerpath) 
            os.mkdir(imagepath) 
        imagelist = os.listdir(imagepath)
        return imagelist


class AddDoc(Resource):
    def post(self, worker_id):
        if request.method == "POST":
            if request.files:
                file_list = request.files.getlist("image[]")
                desc = request.form["type"]
                for image in file_list:
                    img = Image.open(BytesIO(image.read()))
                    w, h = img.size
                    img = img.resize((50+int(w/50), 50+int(h/50)),Image.ANTIALIAS)
                    if allowed_file(image.filename):
                        image_path = os.path.join(app.config["IMAGE_WORKER"], worker_id, desc)
                        if os.path.exists(image_path):
                            image_path = os.path.join(app.config["IMAGE_WORKER"], worker_id, desc)
                        else:
                            os.mkdir(image_path)
                    count = len(AddDoc.filecounters(worker_id,desc))+1
                    image_extension = 'webp'
                    profile_path = os.path.join(image_path, f"{worker_id}-{count}|{desc}.{image_extension}")
                    img.save(profile_path,optimize=True,quality=80)
                    
                flash("Photo upload","success")
                ver_id = userId.uid("ver")
                dbModel.insert("verification",['ver_id','worker_id','message'],[ver_id,worker_id,desc])
                return redirect(f"/worker/profile")
            else:
                flash("Please try again !!","warning")
                return redirect(f"/worker/profile")

    # # @app.route('/get_image', methods=["GET", "POST"])
    # def get():
    #     user_id = request.form['user_id']
    #     image_type = request.form['image_type']
    #     path = app.config["IMAGE_REC"] + f"\\{user_id}"
    #     file_list = os.listdir(path)
    #     ls = [os.path.join(path, x) for x in file_list if image_type in x]
    #     for file in ls:
    #         try:
    #             print(file)
    #             return send_file(file, as_attachment=True)
    #         except:
    #             pass
    #     return "None"


    def filecounters(worker_id, desc):
        APP_FOLDER = "/home/ubuntu/integration/app/static/worker"
        imagepath = os.path.join(APP_FOLDER,worker_id,desc)
        workerpath = os.path.join(APP_FOLDER,worker_id)
        if os.path.exists(imagepath):
            pass
        else:  
            if os.path.exists(workerpath):
                pass
            else:
                os.mkdir(workerpath) 
            os.mkdir(imagepath) 
        imagelist = os.listdir(imagepath)
        return imagelist
