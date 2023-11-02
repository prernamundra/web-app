#checked
from flask.templating import render_template
from flask_restful import Resource
from flask import request,flash
import json

from werkzeug.utils import redirect
from werkzeug.wrappers import Response
#-----------
from models import date
from models import userId
#-----------
from models import lognRes
from models import dbModel
#-------



# list of all worker who applied for perticular job

# @app.route('/show/applied/worker', methods=['POST'])

class AllWorkerApplied(Resource):
    def applicants(work_id):
        try:

            check = dbModel.select("work", ["work_id","date_of_work"], ["work_id"], [work_id])
            date_of_work = str(check[0][1])
            if check != ():
                #check worker id and recruiter id from applied table
                work_tuple = dbModel.select("applied", ["worker_id","recruiter_answer","apply_id"],["work_id"],[work_id])
            

                # try:
                #     worker_list = []
                #     for l in work_tuple:
                #         lis = [x for x in l]
                #         worker_list.append(lis)
                # except:
                #     flash("No one apply yet","info")
                #     lognRes.idError(work_id)
                #     return 0,0
                    
                ls = []
                
                #if didnt worked then use for a in worker_list
                for a in work_tuple:
                    # Select the required field to the respective worker table
                    all_details = dbModel.select("worker",["type","name","phone","location","worker_id","image","review","verified"],["worker_id"],[a[0]])
                    rec_answer = a[1]
                    apply_id = a[2]
                    all_details = list(all_details[0])
                    all_details.append(rec_answer)
                    all_details.append(apply_id)
                    all_details = tuple(all_details)
                    ls.append(all_details)
                    lognRes.successful(ls,ls)
                ls =tuple(ls)
                return ls,date_of_work
            else:
                flash("No one apply yet","info")
                lognRes.idError(work_id)
                return 0,0
             
                
        except:
            flash("No one apply yet","info")
            lognRes.unExpected()
            return 0,0
           

