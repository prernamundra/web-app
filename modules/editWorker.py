#checked
from flask_restful import Resource
from flask import request,Response, render_template,flash,redirect,send_from_directory, abort, send_file,jsonify,session
import json
#-----------
from models import date
from models import userId
from config.setup import app
#-----------
from models import lognRes
from models import dbModel
#---------
from werkzeug.utils import secure_filename
import os

from PIL import Image
from io import BytesIO

app.config["IMAGE_REC"] = "/home/ubuntu/integration/app/static/recruiter"
app.config["IMAGE_WORKER"] = "/home/ubuntu/integration/app/static/worker"

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

class EditWorker(Resource):
    def get(self):
        if session.get("id") is not None:
            worker_id = session.get("id")
        else:
            return redirect('/login/worker')
        if type(worker_id) is str and len(worker_id) != 0:
            all_details = dbModel.select("worker",["location", "address", "image", "name"],["worker_id"], [worker_id])
            if all_details != ():
                cur_url = request.url
                back_url = request.referrer
                msg = "Edit Profile"
                lognRes.successful(all_details, all_details)
                return Response(render_template('Edit_Worker.html',profile = all_details[0],worker_id=worker_id,back_link = back_url,nav_title = msg,cur_url=cur_url),mimetype='text/html')
            else:
                lognRes.idError(worker_id)
                flash("please try again !!","warning")
                return redirect('/worker/profile'.format(worker_id)) 
        else:
            lognRes.valueError(worker_id)
            return redirect('/worker/profile'.format(worker_id))
    def post(self):

        try:
            if session.get("id") is not None:
                worker_id = session.get("id")
            else:
                return redirect('/login/worker')
            # lognRes.posting(["worker_id","address","location","image","name"])
            data = {}   
            try:
                # storing post data
                data = request.form
                data = json.dumps(dict(data))
                data = json.loads(data)
            except:
                flash("please try again !!","warning")
                lognRes.postError()
                return redirect('/edit/worker')

            try:
                # assigning variables to the field values
                address = data['address']
                location = str(data['latitude']) + "," + str(data['longitude'])
                
                image = request.files.getlist('image[]')
                # if len(image) == 0:
                #     image = ['/home/ubuntu/integration/app/static/images/profile.jpg']
                name = data['name']
            except:
                flash("please try again !!","warning")
                lognRes.fieldError(worker_id)
                return redirect('/edit/worker')

            # type and length checking
            if ((type(worker_id) is str) and (type(address) is str) and (type(name) is str) and (type(location) is str) and (
                    len(worker_id) and len(name) and len(address) != 0) and all(chr.isalpha() or chr.isspace() for chr in name)):
                    check = dbModel.select("worker", ["worker_id","image"], ["worker_id"], [worker_id])
                    if check !=() :
                        try:
                            EditWorker.upload_image(image,worker_id)
                        except:
                            pass
                        dbModel.update("worker",["location", "address", "name"],[location, address, name],["worker_id"],[worker_id])
                        lognRes.successful(worker_id,"data updated")
                        flash("update successfully !!","success")
                        return redirect('/worker/profile')
                    else:
                        flash("please try again !!","warning")
                        lognRes.idError(worker_id)
                        return redirect('/edit/worker')
            else:
                flash("please try again !!","warning")
                lognRes.valueError(worker_id)
                return redirect('/edit/worker')
        except:
            flash("please try again !!","warning")
            lognRes.unExpected()
            return redirect('/edit/worker')

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def upload_image(image,worker_id):
        file_list = image   
        user_id = worker_id
        # image_type = request.form["image_type"]
        for image in file_list:
            img = Image.open(BytesIO(image.read()))
            img = img.resize((64,64),Image.ANTIALIAS)
            if EditWorker.allowed_file(image.filename):
                # if "worker" in user_id:
                image_path = os.path.join(app.config["IMAGE_WORKER"], user_id)
                # else:
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
    

        
   