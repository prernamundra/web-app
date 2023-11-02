#checked  - file currently not in use

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


# #For worker hiring rate
# @app.route('/worker/hiringrate', methods=['POST'])
class HiringRate(Resource):
    def post(self):
        try:
            data = {}
            mon = str(date.month())
            try:
                data = request.get_json()
            except:
                return lognRes.postError()
            try:
                worker_id = data['worker_id']
            except:
                return lognRes.fieldError(data)

            if (type(worker_id) is str) and (len(worker_id) != 0):

                if dbModel.select("worker", ["worker_id"],["worker_id"],[worker_id]) != ():                   
                    # Select the required field to the respective applied table
                    count1 = dbModel.select("applied", ["COUNT(*)"],["worker_id","month(apply_date)"],[worker_id,mon])
                    x = count1[0][0]
                    # Select the required field to the respective applied table
                    count2 = dbModel.select("applied", ["COUNT(*)"],["worker_id","recruiter_answer","month(apply_date)"],[worker_id,"0",mon])
                    y = count2[0][0]
                    if x == 0:
                        return lognRes.successful(data,"This one is not hiered in this month")
                    z = (y * 100) / x
                    z = "{:.2f}".format(z)
                    return lognRes.successful(z, z)
                else:
                    return lognRes.idError(data)
            else:
                return lognRes.valueError(data)
        except:
            return lognRes.unExpected()
