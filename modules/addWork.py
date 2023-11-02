from lib2to3.pgen2.token import GREATER
from flask_restful import Resource
from flask import request,Response, render_template,flash,redirect,send_from_directory, abort, send_file,jsonify, session
import json
#-----------
from models import date
from datetime import datetime, time
from models import userId
#-----------
from models import lognRes
from models import dbModel
#--------- 
from config.setup import app
#---------
import os
from modules import recruiterWorkDetails
from werkzeug.utils import secure_filename

from PIL import Image
from io import BytesIO


app.config["IMAGE_REC"] = "/home/ubuntu/integration/app/static/recruiter"
app.config["IMAGE_WORKER"] = "/home/ubuntu/integration/app/static/worker"

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
# global dic_type_count_work
# dic_type_count_work = db.count_work



# to check job post date is between start date and end date
def check_add_work(de, c, sd, ed, work_id, rec_id, data):
    de = str(de)
    sd = str(sd)
    ed = str(ed)
    if (datetime.strptime(sd, "%Y-%m-%d %H:%M:%S") <= datetime.strptime(de, "%Y-%m-%d %H:%M:%S") <= datetime.strptime(ed, "%Y-%m-%d %H:%M:%S")):
        l = 10
        if c >= l:
            flash("Work post request exceed !!","danger")
            sus_id = userId.uid("sus")
            message = f'recruiter post jobs out of limit {l}'
            assigned_to = "Shivam Gupta"
            dbModel.insert("suspicious",["work_id","rec_id","sus_id","message","assigned_to"],[work_id,rec_id,sus_id,message,assigned_to])
        else:
            pass
        return True
    else:
        return False

# # To Add work 
# @app.route('/add/work', methods=['POST'])
class AddWork(Resource):
    def get(self):
        if session.get("id") is not None:
            rec_id = session.get("id")
        else:
            return redirect('/login/rec')
        cur_url = request.url
        back_url = request.referrer
        msg = "Add Work"
        return Response(render_template('add_job.html',rec_id=rec_id,back_link = back_url,nav_title = msg,cur_url=cur_url),mimetype='text/html')

    def post(self):
        # global dic_type_count_work
        try:
            if session.get("id") is not None:
                rec_id = session.get("id")
            else:
                return redirect('/login/rec')
            date_entry = str(date.nowDate())

            try:
                data = request.form
                data = json.dumps(dict(data))
                data = json.loads(data)
                print("My work data  \n",data)
            except:
                lognRes.postError()
                flash("please try again","warning")
                return redirect('/add/work')

            work_id = userId.uid("work")
            try:
                # assigning variables to the field values
                rec_id = rec_id
                title = data['title']
                location = str(data['latitude']) + "," + str(data['longitude'])
                date_of_work = data['date_of_work']
                amount = str(data['amount_from']) +"-"+ str(data['amount_to'])
                print(amount)
                dur_work = data['duration_of_work']
                req_workers = int(data['req_workers'])
                address = data['address']
                work_type = data['type']
                desc = data['description']
                alt_no = int(data['alt_no'])
                image = request.files.getlist('image[]')
            except:
                lognRes.fieldError(data)
                flash("please try again !!","warning")
                return redirect('/add/work')


            # type and length checking
            if (((type(address) is str) and (type(desc) is str) and (type(work_type) is str) and (type(location) is str) and (type(req_workers) is int) and (
                    type(amount) is str) and (type(alt_no) is int) and (type(rec_id) is str)) and (
                    len(desc) and len(work_type) and len(rec_id) is not None) and all(chr.isalpha() or chr.isspace() for chr in work_type) and req_workers >= 1):

                get_data = dbModel.select("recruiter", ["total_work_count","work_count","str_date","end_date"], ["rec_id"], [rec_id])

                try:
                    # fetch the data from rec table and store in get_data varabile
                    tcount = get_data[0][0]
                    tcount = tcount + 1
                    count = get_data[0][1]
                    count = count + 1
                    str_date = get_data[0][2]
                    end_date = get_data[0][3]
                except:
                    lognRes.idError(data)
                    flash("please try again","warning")
                    return redirect('/add/work')
                
                # For check job post date
                if check_add_work(date_entry, count, str_date, end_date, work_id, rec_id,data):
                    pass
                else:
                    # if the work post date is not in between the start date and end date then start date is now date and end date is 7 days after now date
                    str_date, end_date = date.week()
                    count = 1

                if dbModel.update("recruiter",["str_date","end_date","total_work_count","work_count"],[str_date,end_date,tcount,count], ["rec_id"], [rec_id])[0]:
                    pass
                else:
                    lognRes.dbError(data)
                    flash("please try again","warning")
                    return redirect('/add/work')

                if AddWork.upload_image(image, work_id, rec_id):
                    dbModel.insert("work",["type", "description", "address", "alt_no", "amount", "req_workers", "date_of_entry", "work_id", "rec_id", "duration_of_work", "location", "date_of_work", "deletion_status","title"],[work_type, desc, address, alt_no, amount, req_workers, date_entry, work_id, rec_id, dur_work, location, date_of_work,"0",title])
                    lognRes.successful(data,"data inserted")
                    flash("Work Posted","success")
                    return redirect('/rec/work/detail')
                else:
                    lognRes.dbError(data)
                    flash("please try again","warning")
                    return redirect('/add/work')
            else:
                lognRes.valueError(data)
                return redirect('/add/work')
        except:
            lognRes.unExpected()
            flash("please try again","warning")
            return redirect('/add/work')

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def upload_image(image,work_id,rec_id):
                file_list = image
                user_id = rec_id
                user_work_id = work_id
                # image_type = request.form["image_type"]
                count = 0
                

                recimagepath = os.path.join(app.config["IMAGE_REC"],user_id,"Addwork",user_work_id)
                addworkpath = os.path.join(app.config["IMAGE_REC"],user_id,"Addwork")
                addrecpath = os.path.join(app.config["IMAGE_REC"],user_id)
                if os.path.exists(recimagepath):
                    pass
                else:
                    if os.path.exists(addworkpath):
                        pass
                    else:
                        if os.path.exists(addrecpath):
                            pass
                        else:
                            os.mkdir(addrecpath)
                        os.mkdir(addworkpath)   
                    os.mkdir(recimagepath)


                for image in file_list:
                    img = Image.open(BytesIO(image.read()))
                    w, h = img.size
                    img = img.resize((50+int(w/50), 50+int(h/50)),Image.ANTIALIAS)
                    count += 1
                    if AddWork.allowed_file(image.filename) and count <= 5:
                        if "rec" in user_id:
                            image_path = os.path.join(app.config["IMAGE_REC"], user_id,"Addwork", user_work_id)
                        else:
                            if os.path.exists(image_path):
                                image_path = os.path.join(app.config["IMAGE_REC"], user_id,"Addwork", user_work_id)
                            else:
                                os.mkdir(image_path)
                        # image_extension = image.filename.split(".")[-1]
                        image_extension = 'webp'
                        profile_path = os.path.join(image_path, f"{user_work_id}-{count}.{image_extension}")
                        img.save(profile_path,optimize=True,quality=80)
                lognRes.successful(image,"Successful Image Upload")
                return True

# @app.route("/count/work" , methods=['GET' , 'POST'])
# def count_work():
#     #total_work = 0
#     #for x in dic_type_count_work:
#     #total_work = total_work + dic_type_count_work[x]

#     total_work = sum(dic_type_count_work.values())
#     return jsonify({"result": "success", "status": 200, "total work":total_work, "Dictionary of work type count": dic_type_count_work})
