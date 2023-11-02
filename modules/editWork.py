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
#---------
from config.setup import app
#---------
import os
from modules import addWork
from werkzeug.utils import secure_filename
from modules import notification

class EditWork(Resource):
    def get(self,work_id):
        if session.get("id") is not None:
            rec_id = session.get("id")
        else:
            return redirect('/login/rec')
        if type(work_id) is str and len(work_id) != 0:
                all_details = dbModel.select("work",["type", "description", "alt_no", "address", "amount", "duration_of_work", "req_workers", "DATE(date_of_work)", "work_id","title","location"],["work_id"], [work_id])
                if all_details != ():
                    lognRes.successful(all_details, all_details)
                    cur_url = request.url
                    back_url = request.referrer
                    msg = "Edit Work"
                    return Response(render_template('edit_work.html',work = all_details[0],rec_id=rec_id,back_link = back_url,nav_title = msg,cur_url=cur_url),mimetype='text/html')
                else:
                    flash("please try again !!","warning")
                    lognRes.idError(work_id)
                    return redirect('/edit/work/{}'.format(work_id))
        else:
            flash("please try again !!","warning")
            lognRes.valueError(work_id)
            return redirect('/edit/work/{}'.format(work_id))
    def post(self,work_id):
        try:
            if session.get("id") is not None:
                rec_id = session.get("id")
            else:
                return redirect('/login/rec')
             # lognRes.posting(["work_id","date_of_work","amount","req_workers","location","address","desc","dur_work","alt_no"])

            try:
                # storing post data
                data = request.form
                data = json.dumps(dict(data))
                data = json.loads(data)
                print(data)
            except:
                lognRes.postError()
                flash("please try again !!","warning")
                return redirect('/rec/work/detail')


            try:
                # assigning variables to the field values
                # work_id = data['work_id']
                date_of_work = data['date_of_work']
                location = str(data['latitude']) + "," + str(data['longitude'])
                amount = str(data['amount_from']) +"-"+ str(data['amount_to'])
                print(amount)
                dur_work = data['duration_of_work']
                req_workers = int(data['req_workers'])
                address = data['address']
                desc = data['description']
                alt_no = int(data['alt_no'])
                work_type = data['type']
                title = data['title']
                image = request.files.getlist('image[]')
            except:
                lognRes.fieldError(work_id+rec_id)
                flash("please try again !!","warning")
                return redirect('/edit/work/{}'.format(work_id))
            # type and length checking
            if (((type(address) is str) and (type(desc) is str) and (type(location) is str) and (
                    type(req_workers) is int) and (
                        type(amount) is str) and (type(alt_no) is int) and (type(work_id) is str)) and (
                    len(desc) and len(work_id) != 0) and req_workers >= 1):
                
                    # Updating the required fields to the respective rec row
                if addWork.AddWork.upload_image(image, work_id, rec_id):
                    if dbModel.update("work",["description","alt_no","address","amount","duration_of_work","req_workers","date_of_work","location","type","title"],[desc, alt_no, address, amount, dur_work, req_workers, date_of_work, location,work_type,title],["work_id"],[work_id]):
                        get_id = dbModel.select("applied",["worker_id"], ["work_id"], [work_id])
                        for id in get_id:
                            phone = dbModel.select("worker", ["phone"], ["worker_id"], [id[0]])[0][0]
                            notification.Notification.CreateNotification(rec_id, id[0], work_id, "WORK EDITED", [title,phone])
                        lognRes.successful(work_id+rec_id,"data updated")
                        flash("update successfully !!","success")
                        return redirect('/work/detail/{}/{}'.format(work_id,rec_id))
                        # return redirect('/rec/work/detail')
                    else:
                        flash("please try again !!","warning")
                        lognRes.dbError(work_id+rec_id)
                        return redirect('/edit/work/{}'.format(work_id)) 
                else:
                    flash("please try again !!","warning")
                    lognRes.dbError(work_id+rec_id)
                    return redirect('/edit/work/{}'.format(work_id)) 

            else:
                flash("please try again !!","warning")
                lognRes.valueError(work_id+rec_id)
                return redirect('/edit/work/{}'.format(work_id))

        except:
            flash("please try again !!","warning")
            lognRes.unExpected()
            return redirect('/edit/work/{}'.format(work_id))