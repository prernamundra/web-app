from config.db import mysql
from models import lognRes

def func(key, value):
    ls = []
    # for x in dic:
    #     ls1 = []
    #     ls1.append(x)
    #     ls1.append(f"'{dic[x]}'")
    #     ls.append('='.join(ls1))
    for x, y in zip(key, value):
        ls.append(f"{x}='{y}'")
    return ls

def insert(table, key, value):
    try:
        # x = ','.join(list(dic.keys()))
        y = str(value).replace("[","").replace("]","")
        cursor = mysql.connection.cursor()
        cursor.execute(f"INSERT INTO {table} ({','.join(key)}) VALUES ({y});")
        mysql.connection.commit()
        cursor.close()
        return True
    except:
        return lognRes.dbError(0), False

def select(table, col, key, value):
    try:
        cursor = mysql.connection.cursor()
        lognRes.successful(f"{table}, {col}, {key}, {value}", "input to db")
        cursor.execute(f"SELECT {','.join(col)} FROM {table} WHERE ({' AND '.join(str(x) for x in func(key,value))}) ORDER BY sn desc;")
        data = cursor.fetchall()
        lognRes.successful(data, "testing from db")
        return data
    except:
        return lognRes.dbError(0), False
    

def update(table, key, value, key2, value2):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(f"UPDATE {table} SET {','.join(str(x) for x in func(key,value))} WHERE ({' AND '.join(str(x) for x in func(key2,value2))});")
        mysql.connection.commit()
        cursor.close()
        return True, "just_to_make_tuple"
    except:
        return False, lognRes.dbError("update error")


def delete(rec_id,worker_id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM save_list WHERE rec_id = %s and worker_id = %s", [rec_id, worker_id])
        mysql.connection.commit()
        cursor.close()
    except:
        return lognRes.dbError(0), False

def DeleteNotification(key,id):
    try:
        cursor = mysql.connection.cursor()
        if "rec" in key:
            cursor.execute("DELETE FROM notification WHERE rec_id = %s", [id])
        else:
            cursor.execute("DELETE FROM notification WHERE worker_id = %s", [id])
        mysql.connection.commit()
        cursor.close()
    except:
        return lognRes.dbError(0), False

def selectLike(table,col,key,value):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(f"SELECT {','.join(col)} FROM {table} WHERE concat({','.join(key)}) like '%{value}%' ORDER BY sn desc;")
        data = cursor.fetchall()
        return data
    except:
        return lognRes.dbError(0), False


def selectUnion(table,col,key,value,table1,col1,key1,value1):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(f"SELECT {','.join(col)} FROM {table} WHERE ({' AND '.join(str(x) for x in func(key,value))}) UNION SELECT {','.join(col1)} FROM {table1} WHERE ({' AND '.join(str(x) for x in func(key1,value1))});")
        data = cursor.fetchall()
        return data
    except:
        return lognRes.dbError(0), False