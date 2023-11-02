#checked
from boto3.compat import rename_file
from flask.templating import render_template
from flask_restful import Resource
from flask import request, Response
from werkzeug.utils import redirect
from models import dbModel, lognRes, sms_service
import random

class send_otp(Resource):
    def get(self, type,phone):
        #otp = random.randint(1000,9999)
        otp = 1000
        otp_message = f"Dear custmer, your One Time Password is {otp}."
        if "False" in str(dbModel.insert("otp", ["phone", "otp"], [phone, otp])):
            dbModel.update("otp", ["otp"], [otp], ["phone"],[phone])
        #sms_service.send(phone, otp_message)
        # return Response(render_template("loginotp.html", phone = phone, type=type),mimetype='text/html')
        return redirect(f'/verify/otp/{type}/{phone}')

class otpPage(Resource):
    def get(self, type,phone):
        if type == "recruiter":
            msg = "Recruiter Login"
        else:
            msg = "Worker Login"
        return Response(render_template("loginotp.html", phone = phone, type=type,nav_title=msg),mimetype='text/html')
