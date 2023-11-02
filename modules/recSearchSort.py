#checked
from flask_restful import Resource
from flask import request,Response, render_template,flash,redirect, session
import json

from werkzeug.utils import redirect
from werkzeug.wrappers import Response
#-----------
from models import date
from models import userId
#-----------
from models import lognRes
from models import dbModel
from modules import workerPublicProfile
#---------

class RecSearchSort(Resource):
    def get(self,search_data_list):
        try:
            if session.get("id") is not None:
                rec_id = session.get("id")
            else:
                return redirect('/login/rec')
            search_data_list = search_data_list.split(" ")
            #fetching one search_data from the list
            for search_data in search_data_list:
                search_data = search_data.strip()
                # type and length checking
                all_details = dbModel.selectLike("worker",["type", "name", "phone", "location", "worker_id", "image", "review","verified"],["name","type","phone"],search_data)
                if all_details != ():
                    lognRes.successful(all_details,all_details)
                    status = workerPublicProfile.WorkerPublicProfile.status1(all_details[0][4], date.nowDate())
                    return Response(render_template('worker_card.html',searches = all_details,now = date.nowDate(),rec_id=rec_id,data=search_data_list,status=status),mimetype='text/html')
                else:
                    flash("No worker available !!","danger")
                    lognRes.dbError(search_data_list)
                    return redirect(f'/rec/dashboard')    
        except:
            flash("Please try again !!","danger")
            lognRes.unExpected()
            return redirect(f'/rec/dashboard')
