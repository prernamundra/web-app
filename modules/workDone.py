#checked - relationship db query so to not update data everywhere. Unneccessaary updates to multiple table
from logging import log
from flask_restful import Resource
from flask import request
from flask import request,Response, render_template,flash,redirect,session
from collections import Counter
import json
#-----------
from models import date
from datetime import datetime
from models import userId
#-----------
from models import lognRes
from models import dbModel
from modules import notification

class WorkDone(Resource):
    def get(self,work_id,status):
        try:
            complete_date = date.nowDate()
            if session.get("id") is not None:
                rec_id = session.get("id")
            else:
                return redirect('/login/rec')
            get_data = dbModel.select("work", ["work_status","title"], ["work_id"], [work_id])
                
            if get_data[0][0] == 0:
                lognRes.idError(rec_id)
                flash("Work already done!!","info")
                return redirect('/rec/work/detail')
            else:
                dbModel.update("work",["work_status","completion_date"],[status,complete_date], ["work_id"], [work_id])
                dbModel.update("applied",["work_status"],[status], ["work_id","rec_id"], [work_id,rec_id])
                check = dbModel.select("applied",["worker_id","apply_id"], ["work_id","rec_id","recruiter_answer"], [work_id,rec_id,'0'])
                lognRes.successful(check, "testing")
                name = dbModel.selectUnion("worker", ["name", "phone"], ["worker_id"],[check[0][0]],"recruiter",["name","phone"],["rec_id"],[rec_id])
                print(check, "...\n",name)
                for id in check:
                    notification.Notification.CreateNotification(rec_id, id[0], id[1], "WORK COMPLETED FOR REC", [get_data[0][1],name[0][0],name[1][1]])
                    notification.Notification.CreateNotification(rec_id, id[0], id[1], "WORK COMPLETED FOR WORKER", [get_data[0][1],name[1][0], name[0][1]])
                lognRes.successful(rec_id+work_id, "status updated")
                flash("Work done!!","success")
                return redirect('/rec/work/detail')
        except:
            lognRes.unExpected()
            flash("Please Try Again !!","warning")
            return redirect('/rec/work/detail')
