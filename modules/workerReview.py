from logging import log
from flask_restful import Resource
from flask import request,flash
from collections import Counter
#-----------
from models import date
from models import userId
#-----------
from models import lognRes
from models import dbModel
#---------
from modules import notification

# global rec_r_count

# rec_r_count = db.rec_review_count()

class workerReview(Resource):
    def post(self, worker_id,apply_id):
        # global rec_r_count
        data = {}
        try:
            worker_review_date = date.nowDate()
            # worker_review_date = now.strftime("%Y-%m-%d %H-%M-%S")
            try:
                data = request.form
                data = json.dumps(dict(data))
                data = json.loads(data)
            except:
                return lognRes.postError()

            try:
                # assigning variables to the field values
                worker_review = data['worker_review']
                worker_review_message = data['worker_review_message']
            except:
                return lognRes.fieldError(data)

            # For check of type,length and range
            if (type(apply_id) is str) and (type(worker_id) is str) and (type(worker_review) is int) and (
                    type(worker_review_message) is str) and len(apply_id) != 0 and len(
                worker_id) != 0 and worker_review in range(0, 6):
                try:
                    # check worker id from applied table and worker review from review table
                    checks = dbModel.selectUnion("applied",["worker_id","rec_id"],["apply_id"],[apply_id],"review",["check_worker_review","check_rec_review"],["apply_id"],[apply_id])
                    rec_id = checks[0][1]
                    workerid = checks[0][0]
                    status = int(checks[1][0])

                except:
                    return lognRes.idError(data)
                #status is used to check if the fields have already been filled
                if worker_id == workerid and status != 1:
                    try:
                        # Update the required field to the respective worker table

                        dbModel.update("review",["worker_id"," worker_review_date","worker_review","worker_review_message","check_worker_review"],
                                        [worker_id, worker_review_date,worker_review,worker_review_message,1],["apply_id"],[apply_id])

                    except:
                        flash("Please try again !!","warning")
                        return lognRes.dbError(data)

                    try:
                        # Select the review from worker table
                        x = dbModel.select("recruiter",["review"],["rec_id"],[rec_id])[0][0]
                        check = dbModel.selectUnion("recruiter",["review"],["rec_id"],[rec_id],"worker",["name", "phone"],["worker_id"],[worker_id])
                        x = check[0][0]
                        y = (x + worker_review) / 2
                        #can only concatenate tuple (not "int") to tuple
                    except:
                        flash("Please try again !!","warning")
                        return lognRes.dbError(data)

                    try:
                        # Update the review column in the worker table
                        dbModel.update("recruiter",["review"],[y],["rec_id"],[rec_id])                
                    except:
                        flash("Please try again !!","warning")
                        return lognRes.dbError(data)

                else:
                    return lognRes.idError(data)

                # rec_r_count = rec_r_count + 1
                notification.Notification.CreateNotification(rec_id , worker_id, apply_id, "RECRUITER REVIEW",[check[1][0], check[1][1]])
                return lognRes.successful(data,"success")
            else:
                flash("Please try again !!","warning")               
                return lognRes.valueError(data)
        except:
            flash("Please try again !!","warning")
            return lognRes.valueError(data)

# @app.route('/rec/review/count', methods=['POST','GET'])
# def count():
#         global rec_r_count
#         return jsonify({"result": "success", "status": 200, "review_count": rec_r_count})