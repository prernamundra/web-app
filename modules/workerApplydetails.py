#redirect from cancelapplyrequest.py 
from logging import log
from flask_restful import Resource
from flask import request
from flask import request,Response, render_template,flash,redirect,session
from collections import Counter
import json
#-----------
from models import date
from models import userId
#-----------
from models import lognRes
from models import dbModel
#--------- 



# to show all applied work by perticular worker
# @app.route('/apply/detail', methods=['POST'])
class WorkerApplyDetails(Resource):
    def get(self):
        try:
            if session.get("id") is not None:
                worker_id = session.get("id")
            else:
                return redirect('/login/worker')
            # check length and type
            if type(worker_id) is str and len(worker_id) != 0:
                work_tuple = dbModel.select("applied",["work_id","recruiter_answer","rec_id","apply_id","work_status"],["worker_id","delete_status","worker_status"],[worker_id,"0","0"])
                if work_tuple != ():

                    #lis = [x for x2 in work_tuple for x in x2]
                    lis = []
                    for x in work_tuple:
                        ls1 = []
                        
                        if x[1] is None:
                            ls1.append(3)
                        else:
                            ls1.append(x[1])
                        ls1.append(x[0])
                        ls1.append(x[2])
                        ls1.append(x[3])
                        ls1.append(x[4])
                        lis.append(ls1)
                  
                    ls = []
                    for a in lis:
                        
                        try:
                            # Select the required fields to the respective work row
                            all_details = dbModel.select("work", ["type","description","alt_no","address","amount","duration_of_work","req_workers","date_of_work","title","work_id"], ["work_id","deletion_status"],[a[1],"0"])
                            rec_answer = a[0]
                            rec_id = a[2]
                            apply_id = a[3]
                            work_status = a[4]
                            all_details = list(all_details[0])
                            all_details.append(rec_answer)
                            all_details.append(rec_id)
                            all_details.append(apply_id)
                            all_details.append(work_status)
                            all_details = tuple(all_details) 
                            ls.append(all_details)
                        except:
                            pass


                    ls =tuple(ls)
                    
                    lognRes.successful(ls,ls)
                    cur_url = request.url
                    back_url = request.referrer
                    msg = "Applied Jobs"
                    return Response(render_template('Applied_jobs.html',searches = ls,worker_id = worker_id,back_link = back_url,nav_title = msg,cur_url=cur_url),mimetype='text/html')
                else:
                    flash("Please try again !!","warning")
                    lognRes.idError(worker_id)
                    return redirect(f'/worker/dashboard')
            else:
                flash("Please try again !!","warning")
                lognRes.valueError(worker_id)
                return redirect(f'/worker/dashboard')
        except:
            flash("Please try again !!","warning")
            lognRes.unExpected()
            return redirect(f'/worker/dashboard')


