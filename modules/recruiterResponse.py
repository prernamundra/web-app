#checked
from flask_restful import Resource
from flask import request,Response, render_template,flash,redirect
#-----------
from models import date
from datetime import datetime
from models import userId
#-----------
from models import lognRes
from models import dbModel
#--------- 
from modules import notification



# to take the recruiter answer for the applied worker
# @app.route('/answer/work', methods=['POST'])
class RecruiterResponse(Resource):
    def get(self,apply_id,answer,rec_id,work_id):
        try:
            answer_date = str(date.nowDate())
            check = dbModel.select("applied",["apply_id", "worker_id"],["apply_id"], [apply_id])
            check1 = dbModel.select("review",["apply_id"],["apply_id"], [apply_id])
            c = dbModel.selectUnion("recruiter",["name"],["rec_id"],[rec_id],"work",["title"],["work_id"],[work_id])
            worker_phone = dbModel.select("worker", ["phone"], ["worker_id"],[check[0][1]])[0][0]
            try:
                applyid = check1[0][0]
            except:
                applyid=0
            if check ==():
                flash("please try again !!","warning")
                lognRes.idError(apply_id+rec_id+work_id)
                return redirect(f'/work/detail/{work_id}/{rec_id}')
            else:
                if answer == 1:
                    notification.Notification.CreateNotification(rec_id, check[0][1], work_id, "RECRUITER REJECTED", [c[0][0],c[1][0], worker_phone])
                # update the required fields to the respective applied row
                dbModel.update("applied",["recruiter_answer","answer_date"],[answer,answer_date],["apply_id"],[apply_id])
                if answer == 0 and apply_id != applyid:                       
                    # inserted the required fields to the respective review row
                    dbModel.insert("review",["apply_id"],[apply_id])
                    notification.Notification.CreateNotification(rec_id, check[0][1], work_id, "RECRUITER ACCEPTED", [c[0][0],c[1][0], worker_phone])
                    lognRes.successful(apply_id+rec_id+work_id, "data inserted in review & updated in applied")  
                    return redirect('/work/detail/{}/{}'.format(work_id,rec_id)) 
            lognRes.successful(apply_id+rec_id+work_id, "data updated in applied")
            return redirect('/work/detail/{}/{}'.format(work_id,rec_id)) 
        
        except:
            flash("please try again !!","warning")
            lognRes.unExpected()
            return redirect('/work/detail/{}/{}'.format(work_id,rec_id)) 
