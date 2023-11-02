#checked
#redirect from edit worker
from flask_restful import Resource
from flask import request,render_template,redirect,Response,flash, session
import json
#-----------
from models import date
from models import userId
#-----------
from models import lognRes
from models import dbModel
from modules import workerPublicProfile
from modules import image
#---------
class WorkerProfile(Resource):

    def get(self):
        try:
            if session.get("id") is not None:
                worker_id = session.get("id")
            else:
                return redirect('/login/worker')
            
            checks = dbModel.select("worker",["*"],["worker_id"],[worker_id])
            v_count = checks[0][16]
            hirring = workerPublicProfile.WorkerPublicProfile.totalhirring(worker_id)
            r = workerPublicProfile.WorkerPublicProfile.review(worker_id)
            workDone = workerPublicProfile.WorkerPublicProfile.Completeworkcount(worker_id)
            imagelist = image.AddImage.filecounters(worker_id)
            # y = [{'name': check[2], 'phone': check[3], 'image': check[5], 'type': check[8], 'address': check[15],'review': check[7], 'view_count': check[16]} for check in checks]
            # lognRes.successful(y[0],y[0])
            lognRes.successful(checks[0][2],checks[0][2])
            cur_url = request.url
            back_url = request.referrer
            msg = "Profile"
            return Response(render_template('worker_profile.html',profiles = checks,count=v_count,hirring=hirring,reviews=r,totalWork = workDone,worker_id=worker_id,count1=imagelist,back_link = back_url,nav_title = msg,cur_url=cur_url),mimetype='text/html')
            
               
        except:
            flash("Please try again !!","warning")
            lognRes.unExpected()
            return redirect(f'/worker/dashboard')