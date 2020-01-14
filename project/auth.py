'''
Auth function endpoints
'''
from json import dumps
from flask import Blueprint, request, abort
auth = Blueprint('auth', __name__)
import functions.auth_functions

#curl -X POST 127.0.0.1:5000/auth/register -F email=bob@email.com -F password=password -F name_first=Bob -F name_last=Test
@auth.route('/auth/register', methods=['POST'])
def authregister():
    return dumps(functions.auth_functions.auth_register(request.form.get('email'), request.form.get('password'), request.form.get('name_first'), request.form.get('name_last')))

#curl -X POST 127.0.0.1:5000/auth/login -F email=bob@email.com -F password=password
@auth.route('/auth/login', methods=['POST'])
def authlogin():
    return dumps(functions.auth_functions.auth_login(request.form.get('email'), request.form.get('password')))

#curl -X POST 127.0.0.1:5000/auth/logout -F token=token
@auth.route('/auth/logout', methods=['POST'])
def authlogout():
    return dumps(functions.auth_functions.auth_logout(request.form.get('token')))

#curl -X POST 127.0.0.1:5000/auth/passwordreset/request -F email=bob@email.com
@auth.route('/auth/passwordreset/request', methods=['POST'])
def authpasswordresetrequest():
    return dumps(functions.auth_functions.auth_passwordreset_request(request.form.get('email')))

#curl -X POST 127.0.0.1:5000/auth/passwordreset/reset -F reset_code=code -F new_password=password
@auth.route('/auth/passwordreset/reset', methods=['POST'])
def authpasswordresetreset():
    return dumps(functions.auth_functions.auth_passwordreset_reset(request.form.get('reset_code'), request.form.get('new_password')))

@auth.route('/admin/userpermission/change', methods=['POST'])
def adminuserpermission():
    return dumps(functions.auth_functions.admin_userpermission_change(request.form.get('token'), request.form.get('u_id'), request.form.get('permission_id')))
