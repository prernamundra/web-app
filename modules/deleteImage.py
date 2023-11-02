#checked
import os
from flask_restful import Resource
from flask import redirect,session

class Del(Resource):
    def get(self,fname):
        if session.get("id") is not None:
            worker_id = session.get("id")
        else:
            return redirect('/login/worker')
        # wid = fname.split("-")
        # del wid[-1]
        # wid = "-".join(wid)
        path = f"/home/ubuntu/integration/app/static/worker/{worker_id}/gallery/{fname}"
        # os.remove(os.path.join(path,fname))
        os.remove(path)
        return redirect(f'/worker/profile')

