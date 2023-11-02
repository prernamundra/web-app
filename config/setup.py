from flask import Flask, session
import logging
from flask_session import Session

app = Flask(__name__,template_folder="../templates",static_folder="../static")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# from flask_session import Session #pip install flask_session

# app.secret_key = 'xxxx'

# app.config['SESSION_TYPE'] = 'filesystem'  # session a type of filesystem 
# # app.config['SESSION_FILE_DIR'] = '/Users/wupeiqi/PycharmProjects/grocery/96.Flask the new curriculum / component /2.flask-session'  #  the file path 
# app.config['SESSION_FILE_THRESHOLD'] = 500  #  if the number of sessions is greater than that ， it's time to start deleting 
# app.config['SESSION_FILE_MODE'] = 384  #  file permission type 

# app.config['SESSION_PERMANENT'] = True  #  if set to true, close the browser session is failure. 
# app.config['SESSION_USE_SIGNER'] = False  #  whether to send to the browser session cookie value to encrypt 
# app.config['SESSION_KEY_PREFIX'] = 'session:'  #  the prefix of the value stored in session 

# session_vars =  Session(app)


logging.basicConfig(filename='log_file.log',
                    format='%(levelname)s -- %(asctime)s -- %(funcName)s::%(lineno)d -- %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)