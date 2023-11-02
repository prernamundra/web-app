from logging import log
from flask_restful import Resource
from flask import request
from flask import request,Response, render_template,flash,redirect,session
from collections import Counter
import json
#-----------
from models import date
from models import userId
from datetime import datetime
from modules import notification
#-----------
from models import lognRes
from models import dbModel
#--------- 


#to check if the recuiter cancel the work 
def check_cancel(cd,c,sd,ed,work_id,worker_id,rec_id,data):
    cd = str(cd)
    sd = str(sd)
    ed = str(ed)
    if (datetime.strptime(sd, "%Y-%m-%d %H:%M:%S") <= datetime.strptime(cd, "%Y-%m-%d %H:%M:%S") <= datetime.strptime(ed, "%Y-%m-%d %H:%M:%S")):
        l = 10
        if c >= l:
            flash("Cancle Apply request exceed !!","danger")
            sus_id = userId.uid("sus")
            message = f'worker cancle jobs out of limit {l}'
            assigned_to = "Shivam"
            dbModel.insert("suspicious",["sus_id","worker_id","work_id","message","assigned_to","rec_id"],[sus_id,worker_id,work_id,message,assigned_to,rec_id])
            
        else:
            pass
        return True
    else: 
        return False

#to check  the cancel work
# @app.route('/cancel/work', methods=['POST'])
class CancelApplyRequest(Resource):
    def get(self,work_id,rec_id,apply_id):
        try:
            if session.get("id") is not None:
                worker_id = session.get("id")
            else:
                return redirect('/login/worker')
            # data = {}
            cancel_date = str(date.nowDate())

            #check length
            data = [rec_id,worker_id,apply_id,work_id]
            if (len(rec_id) and len(work_id) and len(worker_id) and len(apply_id) != 0):
                
                get_data = dbModel.select("worker", ["total_cancel_count","cancel_count","str_date","end_date","name"], ["worker_id"], [worker_id]) 
                   
                try:
                    tcount = get_data[0][0]
                    tcount += 1
                    count = get_data[0][1]
                    count += 1
                    str_date = get_data[0][2]
                    end_date = get_data[0][3]
            
                except:
                    flash("Please Try Again !!","danger")
                    return lognRes.idError(work_id + rec_id + apply_id + worker_id)
                #for check cancel job
                if check_cancel(cancel_date,count,str_date,end_date,work_id,worker_id,rec_id,data):
                    pass
                else:
                    flash("Please Try Again !!","danger")
                    str_date, end_date = date.week()
                    count = 1
                # updated the required fields to the respective rec row
                
                if dbModel.update("worker",["str_date","end_date","total_cancel_count","cancel_count"],[str_date,end_date,tcount,count], ["worker_id"], [worker_id]):
                    pass
                else:
                    flash("Please Try Again !!","danger")
                    return lognRes.dbError(work_id + rec_id + apply_id + worker_id)
                check = dbModel.select("applied", ["work_id","worker_id","apply_id","rec_id"], ["work_id","worker_id","apply_id","rec_id"], [work_id,worker_id,apply_id,rec_id])
                if check == ():
                    return lognRes.idError(work_id + rec_id + apply_id + worker_id)
                else:
                    if dbModel.update("applied",["worker_status","cancel_date"],["1",cancel_date], ["apply_id"], [apply_id]):
                        flash("request cancel Successfully !!","success")
                        lognRes.successful(work_id + rec_id + apply_id + worker_id, "data updated")
                        phone = dbModel.select("recruiter", ["phone"], ["rec_id"],[rec_id])[0][0]
                        notification.Notification.CreateNotification(rec_id, worker_id, work_id, "WORKER CANCELLED",[get_data[0][4], phone])
                        return redirect("/worker/apply/details".format(worker_id))
                    else:
                        flash("Please Try Again !!","danger")
                        return lognRes.dbError(work_id + rec_id + apply_id + worker_id)  
            else:
                flash("Please Try Again !!","danger")
                return lognRes.valueError(work_id + rec_id + apply_id + worker_id)
        except:
            flash("Please Try Again !!","danger")
            return lognRes.unExpected()
