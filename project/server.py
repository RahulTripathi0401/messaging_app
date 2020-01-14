"""Flask server"""
import sys
import datetime
import pickle
from json import dumps
from flask import Flask, request, abort, jsonify, make_response, send_from_directory
from flask_cors import CORS, cross_origin
from werkzeug.exceptions import HTTPException
from functions.errors import AccessError

APP = Flask(__name__)
APP.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='pycharmers.1531@gmail.com',
    MAIL_PASSWORD='pycharmersCOMP1531'
)

def error_responder(error):
    ''' Error handling for whole server '''
    if isinstance(error, TypeError):
        code_num = 400
        code_type = "TypeError"
    elif isinstance(error, AccessError):
        code_num = 401
        code_type = "AccessError"
    elif isinstance(error, ValueError):
        code_num = 403
        code_type = "ValueError"
    else:
        code_num = 500
        code_type = "System Error"

    response = APP.response_class(
        response=dumps({
            "code": code_num,
            "name": code_type,
            "message": str(error)
        }),
        status=code_num,
        mimetype='application/json'
    )
    return response

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, error_responder)

CORS(APP)
users = {}
channels = {}

file = open("port.txt", "r") 
portNum = int(file.read())

try:
    with open('export.p', 'r') as FILE:
        DATA = pickle.load(open("export.p", "rb"))
        users = DATA['users']
        channels = DATA['channels']
except:
    pass

import auth
import channel
import message
import user

APP.register_blueprint(auth.auth)
APP.register_blueprint(channel.channel)
APP.register_blueprint(message.message)
APP.register_blueprint(user.user)

# @APP.route('/static/<path:path>')
# def send_js(path):
#     response = make_response(send_from_directory('', path))
#     return response

@APP.route('/shutdown', methods=['GET'])
def endserver():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    saviour()
    func()
    return 'bye'

@APP.route('/saveData', methods=['GET'])
def saviour():
    DATA_STRUCTURE = {'users': users, 'channels': channels}
    # print(DATA_STRUCTURE)
    with open('export.p', 'wb') as FILE:
        pickle.dump(DATA_STRUCTURE, FILE)
    return 'saved'

# curl 127.0.0.1:5000/echo/get
@APP.route('/echo/get', methods=['GET'])
def echo1():
    """ Description of function """
    return dumps({
        'echo' : request.args.get('echo'),
    })

# curl -X POST 127.0.0.1:5000/echo/post -F echo=test
@APP.route('/echo/post', methods=['POST'])
def echo2():
    """ Description of function """
    return dumps({
        'echo' : request.form.get('echo'),
    })

if __name__ == '__main__':
    APP.run(port=portNum)
