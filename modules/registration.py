#checked
#redirect from login.py
# from tkinter import Image
from types import DynamicClassAttribute
from flask_restful import Resource
from flask import request,Response, render_template,flash,redirect,send_from_directory, abort, send_file,jsonify,session
import json
#-----------
from models import date
from models import userId
#-----------
from models import lognRes
from models import dbModel
#---------

from config.setup import app
#---------
import os
from werkzeug.utils import secure_filename
from pathlib import Path
from PIL import Image
from io import BytesIO


app.config["IMAGE_REC"] = "/home/ubuntu/integration/app/static/recruiter"
app.config["IMAGE_WORKER"] = "/home/ubuntu/integration/app/static/worker"

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

total_count_rec = 0
total_count_worker = 0
    
class RegisterWorker(Resource):
    def get(self,phone):
        cur_url = request.url
        back_url = request.referrer
        msg = "Welcome"
        return Response(render_template('registration.html',type='worker',phone=phone,back_link = back_url,nav_title = msg,cur_url=cur_url),mimetype='text/html')
    def post(self):
        #global total_count_worker
        #data = {}
        try:
            # lognRes.posting(["name", "phone", "location", "address", "type"])
            try:
                data = request.form
                data = json.dumps(dict(data))
                data = json.loads(data)
            except:
                flash("Please try again !!","warning")
                lognRes.postError()
                return redirect('/login/worker')
            try:
                # assigning variables to the field values
                name = str(data['name'])
                phone = int(data['phone'])
                location = str(data['latitude']) + "," + str(data['longitude'])
                address = str(data['address'])
                work_type = str(data['type'])
                image = request.files.getlist('image[]')
                # if len(image) == 0:
                #     image = ['/home/ubuntu/integration/app/static/images/profile.jpg']
            except:
                flash("Please try again !!","warning")
                lognRes.fieldError(data)
                return redirect("/login/worker")
            # type and length checking
            if (((type(address) is str) and (type(name) is str) and (type(work_type) is str) and (type(location) is str) and (
                    type(phone) is int)) and (len(name) and len(address) != 0) and phone in range(1000000000,10000000000)):
                check = dbModel.select("worker",["worker_id"], ["phone"], [phone])
                if check != ():
                    
                    lognRes.successful(data, "login")
                    return redirect(f'/worker/dashboard/{check[0][0]}')
                else:
                    worker_id = userId.uid("worker")
                    date_of_enroll = str(date.nowDate())
                    str_date, end_date = date.week()
                    if  create_folder(worker_id):
                        try:
                            upload_worker_image(image, worker_id)
                        except:
                            pass
                        dbModel.insert("worker",["str_date","end_date","worker_id","name","phone","location","date_of_enroll","address","type","image"],[str_date, end_date, worker_id, name, phone, location, date_of_enroll, address, work_type,"1"])
                        #total_count_worker += 1
                        lognRes.successful(data, "signup")
                        session["id"] = worker_id
                        return redirect('/worker/dashboard')
                    else:
                        flash("Please try again !!","warning")
                        lognRes.dbError(data)
                        return redirect("/login/worker")
            else:
                flash("Please try again !!","warning")
                lognRes.valueError(data)
                return redirect('/login/worker') 
        except:
            flash("Please try again !!","warning")
            lognRes.unExpected()
            return redirect('/login/worker')

class RegisterRecruiter(Resource):
    def get(self,phone):
        cur_url = request.url
        back_url = request.referrer
        msg = "Welcome"
        return Response(render_template('registration.html',type='recruiter',phone=phone,back_link = back_url,nav_title = msg,cur_url=cur_url),mimetype='text/html')
    def post(self):
        # global total_count_rec


        try:
            # data = {}

            try:
                data = request.form
                data = json.dumps(dict(data))
                data = json.loads(data)
            except:
                flash("Please try again !!","warning")
                lognRes.postError()
                return redirect('/login/rec')
                
            try:
                # assigning variables to the field values
                name = data['name']
                phone = int(data['phone'])
                loc = str(data['latitude']) + "," + str(data['longitude'])
                address = data['address']
                image = request.files.getlist('image[]')
                if image[0].filename == '':
                    lognRes.successful(image, " no no no ")
            except:
                flash("Please try again !!","warning")
                lognRes.fieldError(data)
                return redirect('/login/rec')

            if (((type(address) is str) and (type(name) is str) and (type(loc) is str) and (type(phone) is int)) and ((len(name) and len(address) and len(loc)) != 0) and all(chr.isalpha() or chr.isspace() for chr in name) and phone in range(1000000000,10000000000)):
                
                check = dbModel.select("recruiter",["rec_id"], ["phone"], [phone])
                if check != ():
                    rec_id = check[0][0]
                    lognRes.successful(data, "login")
                    return Response(render_template('recruiter_dashboard.html',rec_id = rec_id),mimetype='text/html')
                else:
                    date_of_enroll = str(date.nowDate())
                    rec_id = userId.uid("rec")
                    str_date, end_date = date.week()
                    if  create_folder(rec_id):
                        try:
                            upload_rec_image(image,rec_id)
                        except:
                            pass
                        dbModel.insert("recruiter",["str_date","end_date","rec_id","name","phone","location","date_of_enroll","address","image"],[str_date, end_date, rec_id, name, phone, loc, date_of_enroll, address,"1"])
                        # total_count_rec += 1
                        lognRes.successful(data, "signup")
                        session["id"] = rec_id
                        return Response(render_template('recruiter_dashboard.html',rec_id = rec_id),mimetype='text/html')
                    else:
                        flash("Please try again !!","warning")
                        lognRes.dbError(data)
                        return redirect('/login/rec')
            else:
                flash("Please try again !!","warning")
                lognRes.valueError(data)
                return redirect('/login/rec')
        
        except:
            flash("Please try again !!","warning")
            lognRes.unExpected()
            return redirect('/login/rec')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_rec_image(image,rec_id):
    file_list = image
    user_id = rec_id
    # image_type = request.form["image_type"]
    for image in file_list:
        img = Image.open(BytesIO(image.read()))
        img = img.resize((64,64),Image.ANTIALIAS)
        if allowed_file(image.filename):
            if "rec" in user_id:
                image_path = os.path.join(app.config["IMAGE_REC"], user_id)
            else:
                
                if os.path.exists(image_path):
                    image_path = os.path.join(app.config["IMAGE_REC"], user_id)
                else:
                    os.mkdir(image_path)
            # image_extension = image.filename.split(".")[-1]
            image_extension = 'webp'
            profile_path = os.path.join(image_path, f"profile-{user_id}.{image_extension}")
            lognRes.successful(profile_path,"Image Upload Path")
            img.save(profile_path,optimize=True,quality=30)
    lognRes.successful(image,"Successful Image Upload")
    return True
        

def upload_worker_image(image,worker_id):
        file_list = image   
        user_id = worker_id
        # image_type = request.form["image_type"]
        for image in file_list:
            img = Image.open(BytesIO(image.read()))
            img = img.resize((64,64),Image.ANTIALIAS)
            if allowed_file(image.filename):
                if "worker" in user_id:
                    image_path = os.path.join(app.config["IMAGE_WORKER"], user_id)
                else:
                    if os.path.exists(image_path):
                        image_path = os.path.join(app.config["IMAGE_WORKER"], user_id)
                    else:
                        os.mkdir(image_path)
                # image_extension = image.filename.split(".")[-1]
                image_extension = 'webp'
                profile_path = os.path.join(image_path, f"profile-{user_id}.{image_extension}")
                img.save(profile_path,optimize=True,quality=30)
        lognRes.successful(image,"Successful Image Upload")
        return profile_path

def create_folder(id):
    if "worker" in id:
        image_path = os.path.join(app.config["IMAGE_WORKER"], id)
    elif "rec" in id:
        image_path = os.path.join(app.config["IMAGE_REC"], id)
    else:
        return False

    os.mkdir(image_path)
    if os.path.exists(image_path):
        return True
    else:
        return False
