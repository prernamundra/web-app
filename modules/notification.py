# checked
from models import date
from models import userId
# -----------
from models import lognRes
from models import dbModel

from flask_restful import Resource
from flask import request, Response, render_template, flash, redirect, session
from models import sms_service
import json


class Notification(Resource):
    def get(self):
        if session.get("id") is not None:
            id = session.get("id")
        else:
            return redirect('/')
        date_seen = str(date.nowDate())
        if "rec" in id:
            try:
                query = dbModel.select("notification", ["*"], ["rec_id"], [id])
            except:
                return redirect(f'/rec/dashboard')
            cur_url = request.url
            back_url = request.referrer
            msg = "Notification"
            try:
                dbModel.update("notification", ["status", "seen_date"], [
                               "0", date_seen], ["rec_id", "status"], [id, "4"])
            except:
                pass

            return Response(render_template('notification_review.html', data=query, rec_id=id, back_link=back_url, nav_title=msg, cur_url=cur_url), mimetype='text/html')
        elif "worker" in id:
            try:
                query = dbModel.select(
                    "notification", ["*"], ["worker_id"], [id])
            except:
                return redirect(f'/worker/dashboard/{id}')
            cur_url = request.url
            back_url = request.referrer
            msg = "Notification"
            try:
                dbModel.update("notification", ["status", "seen_date"], [
                               "0", date_seen], ["worker_id", "seen_date"], [id, "NULL"])
            except:
                pass
            return Response(render_template('notification_review.html', data=query, worker_id=id, back_link=back_url, nav_title=msg, cur_url=cur_url), mimetype='text/html')
        else:
            return redirect(f'/rec/dashboard')

    def CreateNotification(rec_id, worker_id, work_id, message, data):
        domain = "http://13.233.99.184:8080/"
        try:
            date_entry = str(date.nowDate())
            nid = userId.uid("n")

            if "WORKER APPLIED" in message:
                message = f"{data[0]} has applied for work: {data[1]}"
                url = f"/work/detail/{work_id}/{rec_id}"
                sms_service.send(data[2], message)
                worker_id = 0

            elif "WORKER CANCELLED" in message:
                message = f"{data[0]} denied to work."
                url = f"/work/detail/{work_id}/{rec_id}"
                sms_service.send(data[1], message)
                worker_id = 0

            elif "WORKER REVIEW" in message:
                message = f"{data[0]} reviewed you!"
                url = f"/worker/profile"
                sms_service.send(data[1], message)
                rec_id = 0

            elif "RECRUITER REVIEW" in message:
                message = f"{data[0]} reviewed you!"
                url = f"/rec/profile/{rec_id}"
                sms_service.send(data[1], message)
                worker_id = 0

            elif "RECRUITER ACCEPTED" in message:
                message = f"{data[0]} accepted your request for work: {data[1]}"
                url = f"/worker/apply/details/{worker_id}"
                sms_service.send(data[2], message)
                rec_id = 0

            elif "RECRUITER REJECTED" in message:
                message = f"{data[0]} rejected your request for work: {data[1]}"
                url = f"/worker/apply/details/{worker_id}"
                sms_service.send(data[2], message)
                rec_id = 0

            elif "WORK COMPLETED FOR REC" in message:
                message = f"{data[0]} has been completed, Please rate {data[1]}."
                url = f"/rec/work/review/{rec_id}/{work_id}"
                sms_service.send(data[2], message)
                worker_id = 0

            elif "WORK COMPLETED FOR WORKER" in message:
                message = f"Hurray! You have completed the {data[0]} Work, Please rate {data[1]}."
                url = f"/worker/work/review/{worker_id}/{work_id}"
                sms_service.send(data[2], message)
                rec_id = 0

            elif "WORK EDITED" in message:
                message = f"Work: {data[0]} is updated, open application to view the updates made!"
                url = f"/worker/work/detail/{work_id}/{worker_id}"
                sms_service.send(data[1], message)
                rec_id = 0
            else:
                message = f"error Notification!"
                url = "/"
                rec_id = 0
                worker_id = 0
            print(message, url, rec_id, worker_id)
            # type and length checking
            if (type(message) is str):
                print(message, url, rec_id, worker_id)
                if dbModel.insert("notification", ["nid", "rec_id", "worker_id", "message", "notification_date", "url"], [nid, rec_id, worker_id, message, date_entry, url]):
                    lognRes.successful(message, "data inserted")
                else:
                    lognRes.dbError(message)
            else:
                lognRes.valueError(message)
        except:
            lognRes.unExpected()
