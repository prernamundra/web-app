from flask.globals import request
from flask_restful import Api
from flask import render_template,session
from werkzeug.utils import redirect
from config.setup import app
from os import urandom
from time import sleep
from models.userId import uid
from modules import help_support,verification,deleteNotification,sms,notification,registration,login,addWork,allWorkerApplied,apply,call,cancelApplyRequest,deleteSavelist,deleteWork,editRec,editWork,editWorker,hirringRate,recProfile,recruiterRating,recruiterResponse,recruiterReviewForWork,recruiterWorkDetails,recSearchSort,saveList,viewSavelist,workerApplydetails,workerCallCount,workerDashboard,workerProfile,workerPublicProfile, workerShareProfile,workerRating,workerReview,workerSearchSort,workerTotalhirringrate,globalWorkDetails,workerGlobalworkdetail,workDone,image,deleteImage, editimage
app.secret_key = urandom(24)

api = Api(app)

api.add_resource(login.LoginRecruiter, '/login/rec')
api.add_resource(login.LoginWorker, '/login/worker')
api.add_resource(registration.RegisterWorker,'/register/worker' ,'/register/worker/<phone>')
api.add_resource(registration.RegisterRecruiter,'/register/rec', '/register/rec/<phone>')
api.add_resource(apply.ApplyWork, '/apply/work/<details>')
api.add_resource(recProfile.RecProfile, '/recruiter/profile')
api.add_resource(workerProfile.WorkerProfile, '/worker/profile')
api.add_resource(workerSearchSort.WorkerSearchSort, '/worker/search_sort/<search_data_list>')
api.add_resource(recSearchSort.RecSearchSort, '/rec/search_sort/<search_data_list>')
api.add_resource(addWork.AddWork, '/add/work')
api.add_resource(allWorkerApplied.AllWorkerApplied, '/show/applied/worker/<work_id>')
api.add_resource(call.Call, '/call/details')
api.add_resource(cancelApplyRequest.CancelApplyRequest, '/cancel/apply/request/<work_id>/<rec_id>/<apply_id>')
api.add_resource(deleteSavelist.DeleteSavelist, '/delete/savelist/<worker_id>')
api.add_resource(deleteWork.DeleteWork, '/delete/work')
api.add_resource(editRec.EditRec, '/edit/rec')
api.add_resource(editWork.EditWork, '/edit/work/<work_id>')
api.add_resource(editWorker.EditWorker, '/edit/worker')
api.add_resource(hirringRate.HiringRate, '/worker/hiringrate')
api.add_resource(recruiterRating.RecruiterRating, '/rec/rating')
api.add_resource(recruiterResponse.RecruiterResponse, '/answer/work/<apply_id>/<int:answer>/<rec_id>/<work_id>')
api.add_resource(recruiterReviewForWork.RecruiterWorkReview, '/rec/work/review/<rec_id>/<apply_id>')
api.add_resource(recruiterWorkDetails.RecruiterWorkDetail, '/rec/work/detail')
api.add_resource(saveList.SaveList, '/savelist/<worker_id>')
api.add_resource(viewSavelist.ViewSaveList, '/view/savelist')
api.add_resource(workerApplydetails.WorkerApplyDetails, '/worker/apply/details')
api.add_resource(workerCallCount.WorkerRecievedCallCount, '/worker/recieved/callcount')
api.add_resource(workerRating.WorkerRating, '/worker/rating')
api.add_resource(workerTotalhirringrate.WorkerTotalHiringRate, '/worker/total/hiringrate')
api.add_resource(workerDashboard.WorkerDashboard,'/worker/dashboard')
api.add_resource(workerPublicProfile.WorkerPublicProfile,'/worker/profile/public/<rec_id>/<now>/<worker_id>')
api.add_resource(workerShareProfile.WorkerShareProfile,'/worker/profile/share/<rec_id>/<now>/<worker_id>')
api.add_resource(workerReview.workerReview,'/worker/work/review/<worker_id>/<apply_id>')
api.add_resource(globalWorkDetails.WorkDetail,'/work/detail/<work_id>/<rec_id>')
api.add_resource(workerGlobalworkdetail.GlobalWorkDetail,'/worker/work/detail/<work_id>/<worker_id>')
api.add_resource(workDone.WorkDone,'/work/done/<work_id>/<status>')
api.add_resource(image.AddImage,'/worker/image/upload/<worker_id>')
api.add_resource(deleteImage.Del,'/del/image/<fname>')
api.add_resource(notification.Notification,'/notification')
api.add_resource(sms.send_otp, '/send/otp/<type>/<phone>')
api.add_resource(sms.otpPage, '/verify/otp/<type>/<phone>')
api.add_resource(deleteNotification.DeleteNotification, '/delete/notification')
api.add_resource(editimage.EditImage, '/edit/description/<fname>')
api.add_resource(verification.Verification, '/verification')
api.add_resource(help_support.Help_support, '/help_support')
api.add_resource(image.AddDoc, '/worker/doc/upload/<worker_id>')


@app.route('/log')
def stream():
    def generate():
        with open('log_file.log') as f:
            while True:
                yield f.read()
                sleep(1)
    return app.response_class(generate(), mimetype='text/plain')

@app.route("/",methods=['GET','POST'])
def home():
    if session.get("id") is not None:
        uid = session.get("id")
        if 'rec' in uid:
            return redirect("/rec/dashboard")
        return redirect("/worker/dashboard")
    else:
        return render_template("landingpage.html")

@app.route("/logout",methods=['GET','POST'])
def logout():
    if session.get("id") is not None:
        id = session.get("id")
        session["id"] = None
        if 'rec' in id:
            return redirect("/login/rec")
        elif 'worker' in id:
            return redirect("/login/worker")
        else:
            return redirect('/')
    return redirect('/')

@app.route("/rec/dashboard",methods=['GET','POST'])
def rec_dashboard():
    if session.get("id") is None:
        return redirect('/login/rec')
    return render_template("recruiter_dashboard.html",rec_id=session.get("id"))
    
@app.route('/pause')
def pause():
    return render_template('loader.html', form_data=request.form['form_data'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
