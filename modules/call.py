#checked
from flask_restful import Resource
from flask import request
#-----------
from models import date
from models import userId
#-----------
from models import lognRes
from models import dbModel
#--------- 

# global worker_c_count 
# global rec_c_count


# worker_c_count = db.worker_call_count()
# rec_c_count = db.recruiter_call_count()
# print(worker_c_count,rec_c_count)



# to count call details 
# @app.route('/call/details', methods=['POST'])
class Call(Resource):
    def post(self) :
        # global worker_c_count
        # global rec_c_count

        try:
            data = {}
            call_date = str(date.nowDate())

            try:
                data = request.get_json()
            except:
                return lognRes.postError()   

            call_id = userId.uid("call")
            try:
                # assigning variables to the field values
                rec_id = data['rec_id']
                direction = data['direction']
                worker_id = data['worker_id']
            except:
                return lognRes.fieldError(data)

            #type and length check    
            if ((type(worker_id) is str) and (type(rec_id) is str) and (type(call_id) is str) and (type(direction) is str) and (len(worker_id) and len(rec_id) and len(call_id) is not None) and all(chr.isalpha() or chr.isspace() for chr in direction)) :
                    # Select the required fields to the respective recruiter and worker row   
                check1 = dbModel.select("worker", ["worker_id"], ["worker_id"], [worker_id])
                check2 = dbModel.select("recruiter", ["rec_id"], ["rec_id"], [rec_id])
                    
                try:
                    recid = check2[0][0]
                    workerid = check1[0][0]
                except:
                    return lognRes.idError(data)
                # checking rec_id and worker_id    
                if (recid == rec_id ) and (workerid == worker_id):
                    dbModel.insert("call_table",["worker_id", "rec_id", "call_id","call_date", "direction"],[worker_id, rec_id, call_id, call_date, direction])
                    
                        # if direction == "rec to worker":
                        #     rec_c_count = rec_c_count+1
                        #     print(rec_c_count)

                        # else:
                        #     worker_c_count = worker_c_count+1
                        #     print(worker_c_count)

                    return lognRes.successful(data, "data inserted")
                else :
                    return lognRes.idError(data)
            else :
                return lognRes.valueError(data)
        except:
            return lognRes.unExpected()

            
# @app.route('/count/worker/call',methods=['POST','GET'])
# class worker_call_count():
#     def Worker_call():
#         global worker_c_count
#         return jsonify({"result": "success", "status": 200, "Worker_call_count": worker_c_count})

# @app.route('/count/rec/call',methods=['POST','GET'])
# class recruiter_call_count():
#     def reruiter_call():
#         global rec_c_count
#         return jsonify({"result": "success", "status": 200, "rec_call_count": rec_c_count})

        