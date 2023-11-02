#redirect from recruiterResponse.py
from logging import log
from flask_restful import Resource
from flask import request,Response, render_template,flash,redirect
#-----------
from models import date
from datetime import datetime
from models import userId
from modules import allWorkerApplied
#-----------
from models import lognRes
from models import dbModel
#--------- 
import os

#session yet to implement
class WorkDetail(Resource):
    def get(self,work_id,rec_id):
        try:
            # type and length checking
            if type(work_id) is str and len(work_id) != 0:
                all_details = dbModel.select("work",["type", "description", "alt_no", "address", "amount", "duration_of_work", "req_workers","DATE(date_of_work)", "work_id","title", "location"],["work_id"], [work_id])
                if all_details != None:
                    ls = allWorkerApplied.AllWorkerApplied.applicants(work_id)
                    imagecount = WorkDetail.filecounters(rec_id, all_details[0][8])
                    msg = "Work Description"
                    lognRes.successful(all_details, all_details)
                    return Response(render_template('added_work.html',works = all_details[0],rec_id = rec_id,searches = ls[0],now = ls[1],count=imagecount,nav_title = msg),mimetype='text/html')
                else:
                    lognRes.idError(work_id+rec_id)
                    flash("please try again !!","warning")
                    return redirect('/rec/work/detail')
            else:
                flash("please try again !!","warning")
                lognRes.valueError(work_id+rec_id)
                return redirect('/rec/work/detail')
        except:
            flash("please try again !!","warning")
            lognRes.unExpected()
            return redirect('/rec/work/detail')


    def filecounters(rec_id,work_id):
        APP_FOLDER = "/home/ubuntu/integration/app/static/recruiter"
        imagepath = os.path.join(APP_FOLDER,rec_id,"Addwork",work_id)
        addworkpath = os.path.join(APP_FOLDER,rec_id,"Addwork")
        if os.path.exists(imagepath):
            pass
        else:
            if os.path.exists(addworkpath):
                pass
            else:
                os.mkdir(addworkpath)   
            os.mkdir(imagepath) 
        imagelist = os.listdir(imagepath)
        return imagelist