#checked
from flask_restful import Resource
from flask import request,Response, render_template,flash,redirect,send_from_directory, abort, send_file,jsonify,session
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

# app.config["IMAGE_WORKER"] = "/home/ubuntu/integration/app/static/worker"
# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class EditImage(Resource):
    def post(self, fname):
            try:
                if session.get("id") is not None:
                    worker_id = session.get("id")
                else:
                    return redirect('/login/worker')
                desc = request.form["desc"]
                # worker_id = request.form["worker_id"]
                # fname = request.form["fname"]
                desc = desc.strip().replace(" ","|")
                new_fname = fname.split("|")[0] + "|" + desc + "." + fname.split("|")[-1].split(".")[-1]
                old_file = os.path.join(f"/home/ubuntu/integration/app/static/worker/{worker_id}/gallery",fname)
                new_file = os.path.join(f"/home/ubuntu/integration/app/static/worker/{worker_id}/gallery",new_fname)
                os.rename(old_file, new_file)
                # for image in file_list:
                   
                #     if allowed_file(image.filename):
                #         image_path = os.path.join(app.config["IMAGE_WORKER"], worker_id, "gallery")
                #         if os.path.exists(image_path):
                #             image_path = os.path.join(app.config["IMAGE_WORKER"], worker_id, "gallery")
                #         else:
                #             os.mkdir(image_path)
                #     image_extension = 'png'
                #     image.save(os.path.join(image_path, f"{worker_id}|{desc}.{image_extension}"))
                flash("Photo upload","success")
                return redirect(f"/worker/profile")
            except:
                flash("Please try again !!","warning")
                return redirect(f"/worker/profile")