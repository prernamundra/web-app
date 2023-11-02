from logging import log
from flask_restful import Resource
from flask import request
from flask import request,Response, render_template,flash,redirect
from collections import Counter
import json
#-----------
from models import date
from datetime import datetime
from models import userId
from modules import notification
#-----------
from models import lognRes
from models import dbModel
#--------- 


def check_apply(ad, c, sd, ed, work_id, worker_id, details):
    ad = str(ad)
    sd = str(sd)
    ed = str(ed)

    # To check the date is between Start date and End date
    if (datetime.strptime(sd, "%Y-%m-%d %H:%M:%S") <= datetime.strptime(ad, "%Y-%m-%d %H:%M:%S") <= datetime.strptime(ed, "%Y-%m-%d %H:%M:%S")):
        # spamming is limited to  10
        l = 10
        if c >= l:
            flash("Apply request exceed !!","danger")
            # counted as spam::spamming limit count exceeded
            sus_id = userId.uid("sus")
            message = f'worker apply for many jobs {l}'

            # inserting suspicious data in suspicious table
            dbModel.insert("suspicious",["work_id","worker_id","sus_id","message"],[work_id,worker_id,sus_id,message])
        else:
            pass
        return True
    else:
        return False

# when worker applies for work
# @app.route('/apply/work', methods=['POST'])
class ApplyWork(Resource):
    def get(self,details):
        # global total_apply_count,cancelled_apply_count
        try:

            apply_id = userId.uid("apply")
            try:
                details = details.split(",")
                work_id = details[0]
                rec_id = details[1]
                worker_id = details[2]
                # e_amount = data['estimated_amount']
            except:
                lognRes.fieldError(details)
                flash("Please Try Again !!","danger")
                return redirect('/worker/dashboard')
            apply_date = str(date.nowDate())

            # For checking type & length
            if ((type(rec_id) is str) and (type(work_id) is str) and (type(worker_id) is str) and (len(rec_id) and len(work_id) and len(worker_id) != 0)):


                get_data = dbModel.select("worker", ["total_apply_count","apply_count","str_date","end_date", "name"], ["worker_id"], [worker_id])
                try:
                    tcount = get_data[0][0]   
                    tcount += 1
                    count = get_data[0][1]
                    count += 1
                    str_date = get_data[0][2]
                    end_date = get_data[0][3]

                except:
                    lognRes.idError(details)
                    flash("Please Try Again !!","danger")
                    return redirect('/worker/dashboard')


                # For check job post date
                if check_apply(apply_date, count, str_date, end_date, work_id, worker_id, details):
                    pass
                else:

                    # if the work post date is not in between the start date and end date then start date is now date and end date is 7 days
                    str_date, end_date = date.week()
                    count = 1
                    # updated the required fields to the respective rec row
                
                if dbModel.update("worker",["total_apply_count","apply_count","str_date","end_date"],[tcount,count,str_date,end_date], ["worker_id"], [worker_id]):
                    pass
                else:
                    lognRes.dbError(details)
                    flash("Please Try Again !!","danger")
                    return redirect('/worker/dashboard/')

                
                
                # Checking rec_id & work_id
                check = dbModel.select("work", ["work_id","rec_id", "title"], ["work_id","rec_id"], [work_id,rec_id])
                check1 = dbModel.select("applied", ["work_id","rec_id","worker_id"], ["work_id","rec_id","worker_id"], [work_id,rec_id,worker_id])

                if check == ():
                    lognRes.idError(details)
                    flash("Invalid Work !!","danger")
                    return redirect('/worker/dashboard')
                else:
                    if check1 == ():
                        dbModel.insert("applied",["apply_date","apply_id","work_id","rec_id","worker_id","estimated_amount"],[apply_date, apply_id, work_id, rec_id, worker_id,'0'])
                        # cancelled_apply_count += 1
                        # total_apply_count += 1
                        lognRes.successful(details, "data inserted")
                        phone = dbModel.select("recruiter", ["phone"], ["rec_id"],[rec_id])[0][0]
                        notification.Notification.CreateNotification(rec_id, worker_id, work_id, "WORKER APPLIED",[get_data[0][4],check[0][2], phone])
                        flash("Apply Successful !!","success")
                        return redirect('/worker/dashboard')
                    else:
                        lognRes.idError(details)
                        flash("Already Applied !!","info")
                        return redirect('/worker/dashboard')
                        
                # successfully inserted the data and returning
            
            else:
                lognRes.valueError(details)
                flash("Please Try Again !!","danger")
                return redirect('/worker/dashboard')
        except:
            lognRes.unExpected()
            flash("Please Try Again !!","danger")
            return redirect('/worker/dashboard')

# returning global variable of total and cancel apply count
# @app.route("/count/apply", methods=['GET','POST'])
# class countApply():
#     def post(self):
#         return jsonify({'result': "success", 'status': 200, "cancelled_apply": cancelled_apply_count,
#                         "total_apply": total_apply_count})

