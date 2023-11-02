from flask_restful import Resource
from flask import request,flash
from collections import Counter
#-----------
from models import date
from models import userId
#-----------
from models import lognRes
from models import dbModel
from models.counter import count
#---------

class WorkerRating(Resource):
    def post(self):
        try:
            data = {}
            #lognRes.posting(["worker_id"])

            # fetching current date
            month = date.month()

            try:
                # storing post data
                data = request.get_json()
            except:
                flash("Please try again !!","warning")
                return lognRes.postError()

            try:
                # assigning variables to the field values
                worker_id = data['worker_id']
            except:
                flash("Please try again !!","warning")
                return lognRes.fieldError(data)

            # type and length checking
            if ((type(worker_id) is str) and (len(worker_id)!=0)):
                
                if dbModel.select("worker",["worker_id"],["worker_id"],[worker_id]) != ():
                    profile = list(dbModel.select("review",["recruiter_review"],["worker_id","month(recruiter_review_date)"],[worker_id, month - 1]))
                    string = count(profile)
                    return lognRes.successful(string,string)
                else:
                    flash("Please try again !!","warning")
                    return lognRes.idError(data)
            else:
                flash("Please try again !!","warning")
                return lognRes.valueError(data)
        except:
            flash("Please try again !!","warning")
            return lognRes.unExpected()