from flask_restful import Resource
from flask import request,Response, render_template,flash,redirect,send_from_directory, abort, send_file,jsonify, session
import json
#-----------
from models import date
from models import userId
#-----------
from models import lognRes
from models import dbModel
from config.setup import app
#---------
import os
import time

class Verification(Resource):
    def get(self):
        if session.get("id") is not None:
            worker_id = session.get("id")
        else:
            return redirect('/login/worker')
        cur_url = request.url
        back_url = request.referrer
        msg = "Verification Form"
        return Response(render_template('verification.html',worker_id=worker_id,back_link = back_url,nav_title = msg,cur_url=cur_url),mimetype='text/html')
