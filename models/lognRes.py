from flask import request
from config.setup import app

# def fields(data, list):
#     for x in list:
#         if x not in data.keys():
#             return fieldError()
#         dic[x] = data[x]
#         return dic

# def posting(list):
#     try:
#         data = request.get_json()
#         return fields(data, list)
#     except:
#         return postError()

def dbError(data):
    app.logger.exception(f"Database Error::{data}") 
    return {"message": "database error"}, 500

def postError():  
    app.logger.exception(f"Post Request Error")
    return {"message": "post request error"}, 500

def fieldError(data):
    app.logger.exception(f"Invalid Field::{data}")
    return {"message": "invalid fields"}, 500

def successful(data, message):
    app.logger.info(f"Successful::{data}")
    return {"message": message}, 200

def valueError(data):
    app.logger.exception(f"Invalid Value::{data}")
    return {"message": "invalid field values"}, 500

def unExpected():
    app.logger.critical(f"Function Error")
    app.logger.exception(f"Function Error")
    return {"message": "unexpected function error"}, 500

def idError(data):
    app.logger.exception(f"Invalid id or id already exists::{data}")
    return {"message": "invalid id values or id already exists"}, 500