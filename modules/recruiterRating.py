#checked - ERROR
from flask_restful import Resource
from flask import request,session,redirect
#-----------
from models import date
from datetime import datetime
from models import userId
#-----------
from models import lognRes
from models import dbModel
from models.counter import count
#--------- 

#func to give worker rating
# @app.route('/rec/rating', methods=['POST'])
class RecruiterRating(Resource):
    def get(self):
        try:
            data = {}

            try:
                # storing post data
                data = request.get_json()
            except:
                return lognRes.postError()
                # fetching current date
            month = date.month()
            
            if session.get("id") is not None:
                rec_id = session.get("id")
            else:
                return redirect('/login/rec')

            # type and length checking
            if type(rec_id) is str:
                check = dbModel.select("recruiter",["rec_id"],["rec_id"],[rec_id])
                if check != ():
                    try:
                        profile = dbModel.select("review",["worker_review"], ["rec_id","month(worker_review_date)"], [rec_id,month-1])
                        string = count(profile)
                        return lognRes.successful(string,string)
                    except:
                        return lognRes.dbError(data)
                else:
                    return lognRes.idError(data)
            else:
                return lognRes.valueError(data)
        except:
            return lognRes.unExpected()

