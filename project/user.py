'''
User function endpoints
'''
from json import dumps
from flask import request, abort, Blueprint
user = Blueprint('user', __name__)
import functions.users

@user.route('/user/profile', methods=['GET'])
def userprofile():
    return dumps(functions.users.user_profile(request.args.get('token'), request.args.get('u_id')))

@user.route('/user/profile/setname', methods=['PUT'])
def usersetname():
    return dumps(functions.users.user_profile_setname(request.form.get('token'), request.form.get('name_first'), request.form.get('name_last')))

@user.route('/user/profile/setemail', methods=['PUT'])
def usersetemail():
    return dumps(functions.users.user_profile_setemail(request.form.get('token'), request.form.get('email')))

@user.route('/user/profile/sethandle', methods=['PUT'])
def usersethandle():
    return dumps(functions.users.user_profile_sethandle(request.form.get('token'), request.form.get('handle_str')))

@user.route('/users/all', methods=['GET'])
def usersall():
    return dumps(functions.users.users_all(request.args.get('token')))

@user.route('/user/profiles/uploadphoto', methods=['POST'])
def userprofilesuploadphoto():
    return dumps(functions.users.user_profiles_uploadphoto(request.form.get('token'), request.form.get('img_url'),
                 request.form.get('x_start'), request.form.get('y_start'), request.form.get('x_end'),
                 request.form.get('y_end')))
