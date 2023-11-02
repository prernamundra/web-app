from flask_restful import Resource
from flask import request,render_template,flash,redirect,Response, session
#-----------
from models import date
from models import userId
#-----------
from models import lognRes
from models import dbModel
#---------
from modules import recruiterWorkDetails

class WorkerSearchSort(Resource):

    def get(self,search_data_list):
        try:
            if session.get("id") is not None:
                worker_id = session.get("id")
            else:
                return redirect('/login/worker')
            now = date.Date()
            search_data_list = search_data_list.split(" ")  
            ls = []            
            for search_data in search_data_list:
                search_data = str(search_data.strip())
                # to check type and length
                if (type(search_data) is str) and (len(search_data) != 0) and all(chr.isalpha() or chr.isspace() for chr in search_data_list):
                    all_details = dbModel.selectLike("work",["type", "description", "alt_no", "address", "amount", "duration_of_work", "req_workers", "DATE(date_of_work)","rec_id","work_id","title","work_status", "location"],["description","type","title"],search_data)
                    if all_details != ():
                        z = [{'type':check[0],'description':check[1], 'alt_no':check[2],'address':check[3],'amount':check[4], 'duration_of_work':check[5],'req_workers':check[6], 'date_of_work':str(check[7])} for check in all_details]
                        ls.extend(z)
                        ls = [dict(t) for t in {tuple(d.items()) for d in ls}]
                        lognRes.successful(ls,ls)
                        pls = {}
                        for i in range(len(all_details)):
                            pls[all_details[i][9]] = recruiterWorkDetails.RecruiterWorkDetail.filecounters(all_details[i][8], all_details[i][9])
                        return Response(render_template('worker_dashboard.html',works = all_details,worker_id= worker_id,counts=pls,data=search_data_list,dow=now),mimetype='text/html')
                    else:
                        flash("Nothing found !!","danger")
                        lognRes.dbError(worker_id)
                        return redirect(f'/worker/dashboard')
                else:
                    flash("Please try again !!","warning")
                    lognRes.valueError(worker_id)  
                    return redirect(f'/worker/dashboard')    
        except:
            flash("Please try again !!","warning")
            lognRes.unExpected()
            return redirect(f'/worker/dashboard')
