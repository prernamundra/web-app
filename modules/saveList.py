#checked
from flask_restful import Resource
from flask import request, Response, render_template, flash, redirect, session
# -----------
from models import date
from datetime import datetime
from models import userId
# -----------
from models import lognRes
from models import dbModel
# ---------


# worker_s_count = db.worker_save_count()


# Where recruiter save worker profile
# @app.route('/save_list', methods=['POST'])
class SaveList(Resource):
    def get(self, worker_id):
        # global worker_s_count

        try:
            now = date.nowDate()
            if session.get("id") is not None:
                rec_id = session.get("id")
            else:
                return redirect('/login/rec')
            # To check type and len of id's is !=0
            # if ((type(rec_id) is str) and (type(worker_id) is str) and (len(rec_id) and len(worker_id) != 0)):
                # Select the required field to the respective save list table
                # check1 = dbModel.select("save_list", ["worker_id", "rec_id"], [
                #                         "worker_id", "rec_id"], [worker_id, rec_id])
                # try:
                #     if len(check1) != 0:
                #         recid1 = check1[0][1]
                #         workerid1 = check1[0][0]

                #     else:
                #         recid1 = 0
                #         workerid1 = 0

                # except:
                #     flash("Please try again !!", "warning")
                #     lognRes.idError(rec_id+worker_id)
                #     return redirect(f'/worker/profile/public/{rec_id}/{now}/{worker_id}')
                
                # # for recruiter id and worker id
                # if (worker_id != workerid1) and (rec_id != recid1):

                    # Select the required field to the respective save list table
            if dbModel.insert("save_list", ["rec_id", "worker_id", ], [rec_id, worker_id]):
                flash("Worker Saved !!", "success")
                # worker_s_count = worker_s_count+1
                return redirect(f'/worker/profile/public/{rec_id}/{now}/{worker_id}')
            else:
                flash("Please try again !!", "warning")
                lognRes.dbError(rec_id+worker_id)
                return redirect(f'/worker/profile/public/{rec_id}/{now}/{worker_id}')

                # else:
                #     flash("Please try again !!", "warning")
                #     lognRes.idError(rec_id+worker_id)
                #     return redirect(f'/worker/profile/public/{rec_id}/{now}/{worker_id}')
            # else:
            #     flash("Please try again !!", "warning")
            #     lognRes.fieldError(rec_id+worker_id)
            #     return redirect(f'/worker/profile/public/{rec_id}/{now}/{worker_id}')
        except:
            flash("Please try again !!", "warning")
            lognRes.unExpected()
            return redirect(f'/worker/profile/public/{rec_id}/{now}/{worker_id}')


# @app.route('/count/save/worker', methods=['POST','GET'])
# def count():
#     global worker_s_count
#     return jsonify({"result": "success", "status": 200, "save_count": worker_s_count})
