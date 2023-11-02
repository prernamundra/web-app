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

class WorkerShareProfile(Resource):
    def get(self,rec_id,now,worker_id):

        try:
            dow = now

            # type and length checking
            if (type(worker_id) is str and len(worker_id) != 0 and dow != ""):
                try:
                    if "False" in str(dbModel.insert("share", ["rec_id", "worker_id", "count"], [rec_id, worker_id, 1])):
                        dbModel.update("share", ["count"], ["count + 1"], ["rec_id","worker_id"],[rec_id, worker_id])
                    return redirect(f'/worker/profile/public/{rec_id}/{dow}/{worker_id}')
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