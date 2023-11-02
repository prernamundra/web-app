#checked
# redirect from savelist.py
from logging import log
from flask.templating import render_template
from flask_restful import Resource
from flask import request,flash
from werkzeug.utils import redirect
from werkzeug.wrappers import Response
#-----------
from models import lognRes
from models import dbModel
#---------
from modules import image
import os

class WorkerPublicProfile(Resource):
    def get(self,rec_id,now,worker_id):

        try:
            dow = now

            # type and length checking
            if (type(worker_id) is str and len(worker_id) != 0 and dow != ""):
                try:
                    checks = dbModel.select("worker",["*"],["worker_id"],[worker_id])
                    v_count = checks[0][16]
                    v_count = v_count + 1
                    dbModel.update("worker",["view_count"],[v_count],["worker_id"],[worker_id])

                    status = WorkerPublicProfile.status1(worker_id, dow)
                    hirring = WorkerPublicProfile.totalhirring(worker_id)
                    wcount = WorkerPublicProfile.Completeworkcount(worker_id)
                    r = WorkerPublicProfile.review(worker_id)
                    checksave = WorkerPublicProfile.checksavelist(worker_id, rec_id)
                    imagelist = WorkerPublicProfile.filecounters(worker_id)
                    #y = [{'name': check[2], 'phone': check[3], 'image':check[5], 'type':check[8],'address':check[15], 'review':check[7], 'view_count':check[16], 'status': status} for check in checks]
                    lognRes.successful(checks[0][2],checks[0][2])
                    cur_url = request.url
                    cur_url = cur_url.replace("public", "share")
                    back_url = request.referrer
                    msg = "Profile"
                    return Response(render_template('public_worker_profile.html',profile = checks[0],status = status,hirring=hirring,wcount=wcount,reviews = r,rec_id=rec_id,worker_id=worker_id,checksave=checksave,count=imagelist,back_link = back_url,nav_title = msg,cur_url=cur_url,share=True),mimetype='text/html')
                except:
                    flash("Please try again !!","warning")
                    lognRes.idError(rec_id+worker_id)
                    return redirect(f'/rec/dashboard')
            else:
                flash("Please try again !!","warning")
                lognRes.valueError(rec_id+worker_id)
                return redirect(f'/rec/dashboard')
        except:
            flash("Please try again !!","warning")
            lognRes.unExpected()
            return redirect(f'/rec/dashboard')


    def status1(worker_id, dow):
        
        try:
            # type and length checking
            # lis=[]
            checks = dbModel.select("applied",["work_id"],["worker_id","recruiter_answer"],[worker_id,0])
            for work_id in checks:
                try:
                    date_of_work = dbModel.select("work",["DATE(date_of_work)","work_status"],["work_id"],[work_id[0]])
                    date_job = date_of_work[0][0].strftime("%Y-%m-%d")
                    work_status = date_of_work[0][1]
                    # if work_status == 1:
                    if dow == date_job and work_status == 1:
                        return "Busy"
                    else:
                        pass
                    
                except:
                    pass
            return "Avaliable"
            # dow = dow.split(" ")[0]
            # if dow in lis:
            #     return "Busy"
            # else:
            #     return "Avaliable"
        except:
            lognRes.unExpected()
            return "Busy"

    def totalhirring(worker_id):
        try:

            
            x = dbModel.select("applied", ["COUNT(*)"], ["worker_id"],[worker_id])[0][0]
            y = dbModel.select("applied", ["COUNT(*)"], ["worker_id","recruiter_answer"], [worker_id,"0"])[0][0]

            if x == 0:
                return 0

            z = int((y * 100) / x)
            # z = "{:.2f}".format(z)
            # lognRes.successful(z,z)
            return z
            
        except:
            lognRes.unExpected()
            return 0
    
    def Completeworkcount(worker_id):
        try:
            count = dbModel.select('applied',['count(work_status)'],['worker_id','work_status'],[worker_id,0])[0][0]
            if count == 0:
                return 0
            return count
            
        except:
            lognRes.unExpected()
            return 0

    def review(worker_id):
        try:
                check = dbModel.select('review',["rec_id","recruiter_review_message"],['worker_id'],[worker_id])
                if check != ():

                    #lis = [x for x2 in work_tuple for x in x2]
                    lis = []
                    for x in check:
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
                        all_details = dbModel.select("recruiter", ["name","image"], ["rec_id"],[a[0]])
                        rec_review = a[1]
                        all_details = list(all_details[0])
                        all_details.append(rec_review)
                        all_details = tuple(all_details) 
                        ls.append(all_details)

                    ls =tuple(ls)
                    # lognRes.successful(ls,ls)
                    return ls
                else:
                    lognRes.idError("No reviews yet "+worker_id)
                    return 0
            
        except:
            lognRes.unExpected()
            return 0

    def checksavelist(worker_id,rec_id):
              
        check1 = dbModel.select("save_list",["worker_id","rec_id"], ["worker_id","rec_id"], [worker_id,rec_id])
        
        if check1 != ():
            return 0
            
        else:
            return 1
       
    def filecounters(worker_id):
        APP_FOLDER = "/home/ubuntu/integration/app/static/worker"
        imagepath = os.path.join(APP_FOLDER,worker_id,"gallery")
        workerpath = os.path.join(APP_FOLDER,worker_id)
        if os.path.exists(imagepath):
            pass
        else:  
            if os.path.exists(workerpath):
                pass
            else:
                os.mkdir(workerpath) 
            os.mkdir(imagepath) 
        imagelist = os.listdir(imagepath)
        return imagelist