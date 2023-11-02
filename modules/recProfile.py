#checked
from flask_restful import Resource
from flask import request,Response, render_template,flash,redirect, session
import json
#-----------
from models import date
from models import userId
#-----------
from models import lognRes
from models import dbModel
#---------

class RecProfile(Resource):

    def get(self):
        try :
            #lognRes.posting(["rec_id"])
            if session.get("id") is not None:
                rec_id = session.get("id")
            else:
                return redirect('/login/rec')
            try:
                # storing post data
                data = request.form
                data = json.dumps(dict(data))
                data = json.loads(data)
            except:
                flash("please try again !!","warning")
                lognRes.postError()
                return redirect(f'/rec/dashboard')
                
            if((type(rec_id) is str) and (len(rec_id) != 0)): 
                # q = dbModel.select("recruiter",["rec_id"],["rec_id"],[rec_id])
                # if q == ():
                #     flash("please try again !!","warning")
                #     lognRes.idError(data)
                #     return redirect(f'/rec/dashboard')
                # else:
                checks = dbModel.select("recruiter",["name","phone","address","image","review"],["rec_id"],[rec_id])
                if checks is not None:
                    #y = [{'name': check[0], 'phone': check[1], 'address': check[2], 'image': check[3], 'review': check[4]} for check in checks]
                    work_posted = RecProfile.work_posted(rec_id)
                    work_hired = RecProfile.worker_hired(rec_id)
                    worker_review = RecProfile.worker_review(rec_id)
                    lognRes.successful(checks[0],checks[0])
                    cur_url = request.url
                    back_url = request.referrer
                    msg = "Profile"
                    return Response(render_template('Recruiter_profile.html',rec_id=rec_id,profile=checks[0],work_posted=work_posted,work_hired=work_hired,reviews=worker_review,back_link = back_url,nav_title = msg,cur_url=cur_url),mimetype='text/html')
                else:
                    flash("please try again !!","warning")
                    lognRes.dbError(rec_id)
                    return redirect(f'/rec/dashboard')
            else:
                flash("please try again !!","warning")
                lognRes.valueError(rec_id)
                return redirect(f'/rec/dashboard') 
        except:
            flash("please try again !!","warning")
            lognRes.unExpected()
            return redirect(f'/rec/dashboard') 

    def work_posted(rec_id):
        try:
            query = dbModel.select("work",["COUNT(rec_id)"],["rec_id"],[rec_id])
            if query != ():
                return query[0][0]
            else:
                return 0
        except:
            flash("please try again !!","warning")
            lognRes.unExpected()
            return 0 

    def worker_hired(rec_id):
        try:
            query = dbModel.select("applied",["COUNT(recruiter_answer)"],["rec_id","recruiter_answer"],[rec_id,'0'])
            if query != ():
                return query[0][0]
            else:
                return 0 
        except:
            flash("please try again !!","warning")
            lognRes.unExpected()
            return 0

    #relationship query for worker id and image from review table... review-->apply-->worker
    def worker_review(rec_id):
        try:
            query = dbModel.select("review",["worker_id","worker_review_message"],["rec_id","check_worker_review"],[rec_id,"1"])
            if query != ():
                #lis = [x for x2 in query for x in x2]
                lis = []
                for x in query:
                    ls1 = []
                    
                    if x[1] is None:
                        pass
                    else:
                        ls1.append(x[0])
                        ls1.append(x[1])
                        lis.append(ls1)
                ls = []
                for a in lis:
                    # Select the required fields to the respective work row
                    all_details = dbModel.select("worker", ["name","image"], ["worker_id"],[a[0]])
                    worker_message = a[1]
                    all_details = list(all_details[0])
                    all_details.append(worker_message)
                    all_details = tuple(all_details) 
                    ls.append(all_details)
                ls =tuple(ls)
                lognRes.successful(ls,ls)
                return ls
            else:
                lognRes.idError(rec_id)
                return 0
        except:
            lognRes.unExpected()
            return 0