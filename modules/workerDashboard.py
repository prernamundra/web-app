#checked
# redirect from apply.py
from logging import log
from flask.globals import session
from flask_restful import Resource
from flask import request
from flask import request,Response, render_template,flash,redirect,session
from collections import Counter
import json
#-----------
from models import date
from models import userId
#-----------
from models import lognRes
from models import dbModel
#---------
from modules import recruiterWorkDetails

class WorkerDashboard(Resource):
    def get(self):
        try:
            if session.get("id") is not None:
                worker_id = session.get("id")
            else:
                return redirect('/login/worker')
            now = date.Date()
            work_type = dbModel.select("worker",["type"],["worker_id"],[worker_id])
            try:
                work_type = work_type[0][0]
            except:
                flash("Please try again !!","warning")
                lognRes.idError(worker_id)
                return redirect('/login/worker')
            
            all_details = dbModel.select("work",["type", "description", "alt_no", "address", "amount", "duration_of_work", "req_workers", "DATE(date_of_work)","rec_id","work_id","title","work_status", "location"],["type"],[work_type])
            #z = [{'type': check[0], 'description': check[1], 'alt_no': check[2], 'address': check[3], 'amount': check[4],'duration_of_work': check[5], 'req_workers': check[6], 'date_of_work': str(check[7])} for check in all_details]
            pls = {}
            for i in range(len(all_details)):
                pls[all_details[i][9]] = recruiterWorkDetails.RecruiterWorkDetail.filecounters(all_details[i][8], all_details[i][9])
                # pls.append(recruiterWorkDetails.RecruiterWorkDetail.filecounters(all_details[i][8], all_details[i][9]))
            #lognRes.successful(z,z)
            lognRes.successful(all_details,all_details)
            return Response(render_template('worker_dashboard.html',works = all_details,worker_id= worker_id,counts=pls,dow= now),mimetype='text/html')
                

            

            
        except:
            flash("Please try again !!","warning")
            lognRes.unExpected()
            return redirect('/login/worker')