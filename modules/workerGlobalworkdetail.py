#checked
from logging import log
from flask.templating import render_template
from flask_restful import Resource
from flask import request,flash
from werkzeug.utils import redirect
from werkzeug.wrappers import Response
#-----------
from models import date
from datetime import datetime
from models import userId
from modules import allWorkerApplied
#-----------
from models import lognRes
from models import dbModel
#--------- 
from modules import recruiterWorkDetails

class GlobalWorkDetail(Resource):
    def get(self,work_id,worker_id):
        try:
            # type and length checking
            if type(work_id) is str and len(work_id) != 0:
                all_details = dbModel.select("work",["type", "description", "alt_no", "address", "amount", "duration_of_work", "req_workers", "date_of_work", "work_id","title","rec_id","location"],["work_id"], [work_id])
                if all_details != None:
                    image_count = recruiterWorkDetails.RecruiterWorkDetail.filecounters(all_details[0][10], all_details[0][8])
                    lognRes.successful(all_details, all_details)
                    cur_url = request.url
                    back_url = request.referrer
                    msg = "Work Detail"
                    return Response(render_template('job.html',works = all_details[0],worker_id=worker_id,count=image_count,back_link = back_url,nav_title = msg,cur_url=cur_url,share=True),mimetype='text/html')
                else:
                    flash("Please try again !!","warning")
                    lognRes.idError(work_id+worker_id)
                    return redirect('/worker/dashboard')
            else:
                flash("Please try again !!","warning")
                lognRes.valueError(work_id+worker_id)
                return redirect('/worker/dashboard')
        except:
            flash("Please try again !!","warning")
            lognRes.unExpected()
            return redirect('/worker/dashboard')

