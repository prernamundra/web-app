#checked
from flask_restful import Resource
from flask import request, Response, render_template,flash,redirect,session
#-----------
from models import date
from models import userId
#-----------
from models import lognRes
from models import dbModel
#--------- 

#To Delete Savelist
# @app.route('/delete/savelist', methods=['POST'])
class DeleteSavelist(Resource):
    def get(self,worker_id):
        try:
            if session.get("id") is not None:
                rec_id = session.get("id")
            else:
                return redirect('/login/rec')
            # # Type and length checking
            # if ((type(rec_id) is str) and (type(worker_id) is str) and (len(rec_id) and len(worker_id) != 0)):

            #     check = dbModel.select("save_list", ["rec_id","worker_id"], ["rec_id","worker_id"], [rec_id, worker_id])
                
            #     try:
            #         # fetch the data from query and store in varabile
            #         recid = check[0][0]
            #         workerid = check[0][1]
            #     except:
            #         flash("please try again !!","warning")
            #         lognRes.idError(rec_id + worker_id)
            #         return redirect('/view/savelist')

            #     # Checking db data to frontend data
            #     if (recid == rec_id ) and (workerid == worker_id):
            dbModel.delete(rec_id, worker_id)
            return redirect('/view/savelist')
            #     else:
            #         flash("please try again !!","warning")
            #         lognRes.idError(rec_id + worker_id)
            #         return redirect('/view/savelist')
            # else:
            #     flash("please try again !!","warning")
            #     lognRes.valueError(rec_id + worker_id)
            #     return redirect('/view/savelist')
        except:
            flash("please try again !!","warning")
            lognRes.unExpected()
            return redirect('/view/savelist')



