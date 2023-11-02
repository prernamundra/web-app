from flask_restful import Resource
from flask import request
#-----------
from models import date
from models import userId
#-----------
from models import lognRes
from models import dbModel
#--------- 


#For worker's total hiringrate
# @app.route('/worker/totalhiringrate', methods=['POST'])
class WorkerTotalHiringRate(Resource):
    def post(self):
        try:
            data = {}

            try:
                data = request.get_json()
            except:
                return lognRes.postError()

            try:
                worker_id = data['worker_id']
            except:
                return lognRes.fieldError(data)

            #For type and length of worker id
            if (type(worker_id) is str) and (len(worker_id) != 0):

                
                x = dbModel.select("applied", ["COUNT(*)"], ["worker_id"],[worker_id])[0][0]
                y = dbModel.select("applied", ["COUNT(*)"], ["worker_id","recruiter_answer"], [worker_id,"0"])[0][0]

                if x == 0:
                    return lognRes.idError(data)

                z = (y * 100) / x
                z = "{:.2f}".format(z)
                return lognRes.successful(z,z)
            else:
                return lognRes.valueError(data)
        except:
            return lognRes.unExpected()


