#checked
#redirect from addwork.py
# redirect from workdone.py
from logging import log
from flask.templating import render_template
from flask_restful import Resource
from flask import request,flash, session
from werkzeug.utils import redirect
from werkzeug.wrappers import Response
#-----------
from models import date
from datetime import datetime
from models import userId
#-----------
from models import lognRes
from models import dbModel
import time
#--------- 
import os


# to show all the work add by the perticular recruiter
# @app.route('/work/detail', methods=['POST'])
class RecruiterWorkDetail(Resource):

    

    def get(self):
        try:
            if session.get("id") is not None:
                rec_id = session.get("id")
            else:
                return redirect('/login/rec')
            #message- Add this if condition of not none in query only 

            all_details = dbModel.select("work",["type", "description", "alt_no", "address", "amount", "duration_of_work", "req_workers", "date_of_work", "work_id","title","work_status"],["rec_id","deletion_status"], [rec_id,"0"])
            if all_details != ():
                imagecount = RecruiterWorkDetail.filecounters(rec_id, all_details[0][8])
                lognRes.successful(all_details,all_details)
                cur_url = request.url
                back_url = request.referrer
                msg = "Added Work"
                # all_details = RecruiterWorkDetail.long_load(all_details)
                return Response(render_template('rec_work.html',works = all_details,rec_id=rec_id,count=imagecount,back_link = back_url,nav_title = msg,cur_url=cur_url),mimetype='text/html')
            
            else:
                lognRes.idError(rec_id)
                msg = "Added Work"
                # redirect('/rec/dashboard'.format(rec_id))
                return Response(render_template('rec_work.html',works = "Null",rec_id=rec_id,nav_title = msg),mimetype='text/html')
        
        except:
            flash("please try again !!","warning")
            lognRes.unExpected()
            return redirect('/rec/dashboard'.format(rec_id))

    def filecounters(rec_id,work_id):
        APP_FOLDER = "/home/ubuntu/integration/app/static/recruiter"
        imagepath = os.path.join(APP_FOLDER,rec_id,"Addwork",work_id)
        addworkpath = os.path.join(APP_FOLDER,rec_id,"Addwork")
        addrecpath = os.path.join(APP_FOLDER,rec_id)
        if os.path.exists(imagepath):
            pass
        else:
            if os.path.exists(addworkpath):
                pass
            else:
                if not os.path.exists(addrecpath):
                    os.mkdir(addrecpath)
                os.mkdir(addworkpath)   
            os.mkdir(imagepath)
        imagelist = os.listdir(imagepath)
        return imagelist