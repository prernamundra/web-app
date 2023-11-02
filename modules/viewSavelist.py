#checked, message- relationship can be applied
#checked - message relationship db query for getting data of workers from the savelist, savelist-->worker
from flask_restful import Resource
from flask import request,redirect,Response,render_template,flash,session
#-----------
from models import date
from models import userId
#-----------
from models import lognRes
from models import dbModel
#--------- 


# to show all the save worker to the respective recruiter
# @app.route('/view/savelist', methods=['POST'])
class ViewSaveList(Resource):
    def get(self):
        try:
            if session.get("id") is not None:
                rec_id = session.get("id")
            else:
                return redirect('/login/rec')
            
            
            check1 = dbModel.select("save_list", ["worker_id"], ["rec_id"], [rec_id])
            
            # ls = []
            # for x in check1:
            #     ls.append(x[0])
            # ls = list(ls)
            
            lis = []
            for id in check1:
                all_details = dbModel.select("worker",["type", "name", "phone", "location", "worker_id", "image", "review","verified"],["worker_id"],[id[0]])[0]
                lis.append(all_details)
            lis = tuple(lis)
        
            lognRes.successful(lis, lis)
            cur_url = request.url
            back_url = request.referrer
            msg = "Save Worker"
            return Response(render_template('SaveWorker.html',searches = lis,now = date.nowDate(),rec_id=rec_id,back_link = back_url,nav_title = msg,cur_url=cur_url),mimetype='text/html')

           
            
        except:
            flash("Please try again !!","warning")
            lognRes.unExpected()
            return redirect(f'/rec/dashboard')
