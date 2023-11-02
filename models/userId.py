from uuid import uuid1

def uid(type):
    uid = uuid1()
    return f'{type}-{uid}'