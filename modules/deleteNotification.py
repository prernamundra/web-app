#checkedd
from models import date
from models import userId
#-----------
from models import lognRes
from models import dbModel

from flask_restful import Resource
from flask import request,Response, render_template,flash,redirect, session
from models import sms_service
import json

class DeleteNotification(Resource):
    def get(self):
        if session.get("id") is not None:
                id = session.get("id")
        else:
            return redirect('/')
        if "rec" in id:
            dbModel.DeleteNotification("rec_id", id)
            flash("Notification removed successfully!!","success")
            return redirect(f'/notification')
        elif "worker" in id:
            dbModel.DeleteNotification("worker_id", id)
            flash("Notification removed successfully!!","success")
            return redirect(f'/notification')
        else:
            flash("please try again !!","warning")
            return redirect(f'/rec/dashboard')
