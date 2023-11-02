from types import DynamicClassAttribute
from flask_restful import Resource
from flask import request,Response, render_template,flash,redirect,session
from flask_session import Session
import json
#-----------
from models import date
from models import userId
#-----------
from models import lognRes
from models import dbModel, sms_service
#---------

class LoginWorker(Resource):
    def get(self):
        cur_url = request.url
        msg = "Worker Login"
        return Response(render_template('login.html',type='worker',back_link = '/',nav_title = msg,cur_url=cur_url),mimetype='text/html')
    def post(self):
        #data = {}
        try:
            # lognRes.posting(["name", "phone", "location", "address", "type"])
            try:
                data = request.form
                data = json.dumps(dict(data))
                data = json.loads(data)
            except:
                lognRes.postError()
                flash("please try again !!","warning")
                return redirect('/login/worker')
            try:
                # assigning variables to the field values
                phone = int(data['phone'])
                otp = data['otp']
                check_data = dbModel.select("otp", ["otp"] , ["phone"], [phone])
            except:
                lognRes.fieldError(data)
                flash("Incorrect Details","danger")
                return redirect('/login/worker')
            # type and length checking
            if ((otp == check_data[0][0]) and (type(phone) is int) and phone in range(1000000000,10000000000)):
                    check = dbModel.select("worker", ["phone","worker_id"], ["phone"], [phone])
                    if check != ():
                        worker_id = check[0][1]
                        session["id"] = worker_id
                        return redirect('/worker/dashboard')
                    else:
                        lognRes.successful(data,"Registering New User")
                        return redirect('/register/worker/{}'.format(phone))
            else:
                lognRes.valueError(data)
                flash("Invalid OTP","warning")
                return redirect(f'/verify/otp/worker/{phone}')

        except:
            lognRes.unExpected()
            flash("please try again !!","warning")
            return flash("unexpected function error","danger")

class LoginRecruiter(Resource):
    def get(self):
        cur_url = request.url
        msg = "Recruiter Login"
        return Response(render_template('login.html',type='recruiter',back_link= '/',nav_title = msg, cur_url = cur_url),mimetype='text/html')
    def post(self):
        # global total_count_rec
        try:
            # data = {}
            try:
                data = request.form
                data = json.dumps(dict(data))
                data = json.loads(data)
                print(data)
            except:
                flash("please try again !!","warning")
                return lognRes.postError()
                
            try:
                # assigning variables to the field values
                phone = int(data['phone'])
                otp = data['otp']
                check_data = dbModel.select("otp", ["otp"] , ["phone"], [phone])
            except:
                lognRes.fieldError(data)
                flash("please try again !!","warning")
                return redirect("/login/rec")
            if ((otp == check_data[0][0]) and (type(phone) is int) and phone in range(1000000000,10000000000)):
                check = dbModel.select("recruiter", ["phone","rec_id"], ["phone"], [phone])
                if check != ():
                    rec_id = check[0][1]
                    lognRes.idError(data)
                    session["id"] = rec_id
                    #return Response(render_template('recruiter_dashboard.html',rec_id = rec_id),mimetype='text/html')
                    return redirect('/rec/dashboard')
                    # return lognRes.successful(data,"Login Success")
                else:
                    lognRes.successful(data,"Registering New User")
                    return redirect('/register/rec/{}'.format(phone))
            else:
                lognRes.valueError(data)
                flash("Invalid OTP","warning")
                return redirect(f'/verify/otp/recruiter/{phone}')
        
        except:
            flash("please try again !!","warning")
            return lognRes.unExpected()