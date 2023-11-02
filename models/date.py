from datetime import datetime
import datetime as DT


def nowDate():
    now = datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S")
    return now

def Date():
    now = datetime.now()
    now = now.strftime("%Y-%m-%d")
    return now

def week():
    start_date = datetime.strptime(nowDate(), "%Y-%m-%d %H:%M:%S")
    end_date = start_date + DT.timedelta(days=7)
    return str(start_date), str(end_date)

def month():
    now = datetime.now()
    now = now.strftime("%m")
    return int(now)