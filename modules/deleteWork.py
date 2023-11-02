from flask_restful import Resource
from flask import request,session,redirect
#-----------
from models import date
from models import userId
from datetime import datetime
#-----------
from models import lognRes
from models import dbModel
#--------- 


# To Check Job Delete Date is Between Start Date and End Date
def check_delete(dd,c,sd,ed,work_id,rec_id):
    dd = str(dd)
    sd = str(sd)
    ed = str(ed)
    if (datetime.strptime(sd, "%Y-%m-%d %H:%M:%S") <= datetime.strptime(dd, "%Y-%m-%d %H:%M:%S") <= datetime.strptime(ed, "%Y-%m-%d %H:%M:%S")):
        l = 10
        if c >= l:
            sus_id = userId.uid("sus")
            message = f'recruiter out of delete limit {l}'
            assigned_to = "Shivam Gupta"
            dbModel.insert("suspicious",["work_id","rec_id","sus_id","message","assigned_to"],[work_id,rec_id,sus_id,message,assigned_to])
            
        else:
            pass
        return True
    else:
        return False

# To Delete Work
# @app.route('/del/work', methods=['POST'])
class DeleteWork(Resource):
    def post(self):
        try:
            data = {}
            date_of_deletion = str(date.nowDate())

            try:
                #Requesting data from frontend
                data = request.get_json()
            except:
                return lognRes.postError()
            try:
                # assigning variables to the field values
                work_id = data["work_id"]
                if session.get("id") is not None:
                    rec_id = session.get("id")
                else:
                    return redirect('/login/rec')
            except:
                return lognRes.fieldError(data)

            # type and length checking
            if ((type(rec_id) is str) and (type(work_id) is str) and (len(rec_id) and len(work_id) != 0)):

                get_data = dbModel.select("recruiter", ["total_delete_count","delete_count","str_date","end_date"], ["rec_id"], [rec_id])

                try:
                    # fetch the data from rec table and store in get_data varabile
                    count = get_data[0][1]
                    count +=1
                    tcount = get_data[0][0]
                    tcount +=1
                    start_date = get_data[0][2]
                    end_date = get_data[0][3]
   
                except:
                    return lognRes.idError(work_id + rec_id)
                
                if check_delete(date_of_deletion,count,start_date,end_date,work_id,rec_id):
                    pass
                else:
                    # if the work delete date is not in between the start date and end date then start date is now date and end date is 7 days after now date
                    str_date, end_date = date.week()
                    count = 1
                    # updated the required fields to the respective rec row in recruiter table
                dbModel.update("recruiter",["total_delete_count","delete_count","str_date","end_date"],[tcount,count,start_date,end_date],["rec_id"],[rec_id])

                check = dbModel.select("work", ["work_id","rec_id","deletion_status"], ["work_id","rec_id"], [work_id,rec_id])
                if check == ():
                    return lognRes.idError(work_id + rec_id)
                else:
                    status = check[0][2]
                    if status !=1:
                        dbModel.update("work",["date_of_deletion","deletion_status"],[date_of_deletion,"1"],["work_id"],[work_id])
                        dbModel.update("applied",["delete_status"],["1"],["work_id"],[work_id])
                        return lognRes.successful(work_id + rec_id,"data updated")
                    else:
                        return lognRes.idError(work_id + rec_id)
            else:
                return lognRes.valueError(work_id + rec_id)
        except:
            return lognRes.unExpected()

