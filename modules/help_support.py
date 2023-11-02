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

class Help_support(Resource):
    def get(self):
        if session.get("id") is not None:
            uid = session.get("id")
        else:
            return redirect('/')
        cur_url = request.url
        back_url = request.referrer
        msg = "Help and Support"
        return Response(render_template('help_support.html',worker_id=uid,back_link = back_url,nav_title = msg,cur_url=cur_url),mimetype='text/html')
