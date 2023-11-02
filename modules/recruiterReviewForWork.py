#checked - message: notification se worker_id lo and yahan pe uski query run mat karo.. code chota krne keliye
from flask_restful import Resource
from flask import request,flash,redirect,Response,render_template
#-----------
from models import date
from datetime import datetime
from models import userId
#-----------
import json
from models import lognRes
from models import dbModel
#--------- 
from modules import notification


# global worker_r_count

# worker_r_count = db.worker_review_count()

# For review provide by recruiter to particular worker
# @app.route('/rec/job/review', methods=['POST'])
class RecruiterWorkReview(Resource):

    def post(self,rec_id,apply_id):
        # global worker_r_count
        try:
            recruiter_review_date = str(date.nowDate())

            try:
                data = request.form
                data = json.dumps(dict(data))
                data = json.loads(data)
            except:
                lognRes.postError()
                flash("please try again","warning")
                return redirect('/rec/dashboard'.format(rec_id))
                # for all type data
            try:
                # rec_id = data['rec_id']
               
                recruiter_review = int(data['recruiter_review'])
                recruiter_review_message = data['recruiter_review_message']
            except:
                flash("please try again !!","warning")
                lognRes.fieldError(data)
                return redirect('/rec/dashboard'.format(rec_id))

            # For check of type ,length and range
            if (type(apply_id) is str) and (type(rec_id) is str) and (type(recruiter_review) is int) and (type(recruiter_review_message) is str) and len(apply_id) != 0 and len(rec_id) != 0 and recruiter_review in range(0, 6):
               
                # yahan se change hoga
                checks = dbModel.selectUnion("applied", ["worker_id","rec_id"],["apply_id"],[apply_id],"review",["check_rec_review","check_worker_review"],["apply_id"],[apply_id])

                worker_id = checks[0][0]

                dbModel.update("review",["rec_id","recruiter_review_date","recruiter_review","recruiter_review_message","check_rec_review"],[rec_id, recruiter_review_date,recruiter_review,recruiter_review_message,"1"], ["apply_id"],[apply_id])
                check = dbModel.select("recruiter",["name", "phone"],["rec_id"],[rec_id])[0]
                # yahan tak

                # if check == "":
                #     lognRes.idError(data)
                #     return redirect('/rec/dashboard'.format(rec_id))                  
                #     # Select the required field to the respective recruiter table
                # else:    
                #     x = check[0][0]
                #     y = (x + recruiter_review) / 2
                #     dbModel.update("worker",["review"],[y],["worker_id"],[worker_id])
                #     lognRes.successful(data,"data updated")
                notification.Notification.CreateNotification(rec_id, worker_id, apply_id, "WORKER REVIEW",[check[0], check[1]])
                flash("Review Done !!","success")
                return redirect('/rec/dashboard'.format(rec_id))
            else:
                flash("please try again !!","warning")
                lognRes.valueError(data)
                return redirect('/rec/dashboard'.format(rec_id))

        except:
            flash("please try again !!","warning")
            lognRes.unExpected()
            return redirect('/rec/dashboard'.format(rec_id))


# @app.route("/count/rec_review", methods=['GET', 'POST'])
# def rec_review():
#     return jsonify({"result": success, "status": 200, "message": worker_r_count})

