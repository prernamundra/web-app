#checked
from flask_restful import Resource
from flask import request
#-----------
from models import date
from datetime import datetime
from models import userId
#-----------
from models import lognRes
from models import dbModel
#--------- 


# kitne different recruiter ne worker ko call kiya hai
# @app.route('/worker/recieved/call_count', methods=['POST'])
class WorkerRecievedCallCount(Resource):
    def post(self):

        try:
            data = {}

            try:
                # storing post data
                data = request.get_json()
            except:
                return lognRes.postError()

            # fetching current date
            month = str(date.month())
            try:
                # assigning variables to the field values
                #direction = data['direction']
                worker_id = data['worker_id']
            except:
                return lognRes.fieldError(data)

            # type and length checking
            check1 = dbModel.select("worker", ["worker_id"], ["worker_id"], [worker_id])

            if check1 != ():
                check = dbModel.select("call_table", ["DISTINCT(rec_id)"], ["worker_id","direction","month(call_date)"], [worker_id,"rec to worker",month])
                # ls = []
                # for row in check:
                #     ls.append(row[0])
                # ls = list(set(ls))
                # count = len(ls)
                count = len(check)
                return lognRes.successful(count, count)
            else:
                return lognRes.idError(data)                    
           
        except:
            return lognRes.unExpected()

    