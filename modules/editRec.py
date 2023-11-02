from flask_restful import Resource
from flask import request,Response, render_template,flash,redirect,send_from_directory, abort, send_file,jsonify, session
import json
#-----------
from models import date
from models import userId
#-----------
from models import lognRes
from models import dbModel
from config.setup import app
#---------
import os
import time
from werkzeug.utils import secure_filename

from PIL import Image
from io import BytesIO



app.config["IMAGE_REC"] = "/home/ubuntu/integration/app/static/recruiter"
app.config["IMAGE_WORKER"] = "/home/ubuntu/integration/app/static/worker"

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

class EditRec(Resource):
    def get(self):
        if session.get("id") is not None:
                rec_id = session.get("id")
        else:
            return redirect('/login/rec')
        cur_url = request.url
        back_url = request.referrer
        msg = "Edit Profile"
        if type(rec_id) is str and len(rec_id) != 0:
                all_details = dbModel.select("recruiter",["name","location","address","image"],["rec_id"],[rec_id])
                if all_details != ():
                    lognRes.successful(all_details, all_details)
                    return Response(render_template('Edit_Rec.html',rec = all_details[0],rec_id=rec_id,back_link = back_url,nav_title = msg,cur_url=cur_url),mimetype='text/html')
                else:
                    flash("please try again !!","warning")
                    lognRes.idError(rec_id)
                    return redirect('/recruiter/profile')
        else:
            flash("please try again !!","warning")
            lognRes.valueError(rec_id)
            return redirect('/recruiter/profile')
    def post(self):
        
        try:
            if session.get("id") is not None:
                rec_id = session.get("id")
            else:
                return redirect('/login/rec')
            data = {}
            # lognRes.posting(["rec_id", "image", "location", "address", "name"])
            try:
                # storing post data
                data = request.form
                data = json.dumps(dict(data))
                data = json.loads(data)
            except:
                flash("please try again !!","warning")
                lognRes.postError()
                return redirect('/edit/rec'.format(rec_id))

            try:
                # assigning variables to the field values
                # rec_id = data['rec_id']
                address = data['address']
                location = str(data['latitude']) + "," + str(data['longitude'])
                image = request.files.getlist('image[]')
                name = data['name']
            except:
                flash("please try again !!","warning")
                lognRes.fieldError(rec_id)
                return redirect('/edit/rec'.format(rec_id))
                

            # type and length checking
            if ((type(rec_id) is str) and (type(address) is str) and (type(name) is str) and (type(location) is str) and (
                    len(rec_id) and len(name) and len(address) != 0) and all(
                chr.isalpha() or chr.isspace() for chr in name)):
                # Updating the required fields to the respective rec row
                if dbModel.select("recruiter", ["rec_id"], ["rec_id"], [rec_id]) != ():
                    try:
                        EditRec.upload_image(image,rec_id)
                    except:
                        pass
                    dbModel.update("recruiter",["address","location","name"],[address, location, name],["rec_id"],[rec_id])
                    flash("update successfully !!","success")
                    lognRes.successful(data,"data updated")
                    return redirect('/recruiter/profile')
                else:
                    flash("please try again !!","warning")
                    lognRes.idError(rec_id)
                    return redirect('/edit/rec')
            else:
                flash("please try again !!","warning")
                lognRes.valueError(rec_id)
                return redirect('/edit/rec')
        except:
            flash("please try again !!","warning")
            lognRes.unExpected()
            return redirect('/edit/rec')




    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def upload_image(image,rec_id):
                file_list = image
                user_id = rec_id
                # image_type = request.form["image_type"]
                for image in file_list:
                    img = Image.open(BytesIO(image.read()))
                    img = img.resize((64,64),Image.ANTIALIAS)
                    if EditRec.allowed_file(image.filename):
                        # if "rec" in user_id:
                        image_path = os.path.join(app.config["IMAGE_REC"], user_id)
                        # else:
                        if os.path.exists(image_path):
                            image_path = os.path.join(app.config["IMAGE_REC"], user_id)
                        else:
                            os.mkdir(image_path)
                        # image_extension = image.filename.split(".")[-1]
                        image_extension = 'webp'
                        profile_path = os.path.join(image_path, f"profile-{user_id}.{image_extension}")
                        img.save(profile_path,optimize=True,quality=30)
                lognRes.successful(image,"Successful Image Upload")
                return profile_path