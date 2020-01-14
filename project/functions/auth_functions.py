'''
Functions called through the auth routes
'''
import hashlib
import random
import string
import threading
from flask_mail import Mail, Message
import functions.general
import functions.helper_tokens
import functions.helper_users
import functions.classes
import server

def auth_login(email, password):
    '''
    Given a registered users' email and password and generates a valid token for
    the user to remain authenticated
    '''
    if email is None or not isinstance(email, str):
        raise TypeError('email should be a string')
    if password is None or not isinstance(password, str):
        raise TypeError('password should be a string')

    if not functions.general.emailCheck(email):
        raise ValueError('Email is not valid')

    logged_user = -1

    # All emails are being stored in lowercase, so email check should do the same
    for key in server.users:
        if server.users[key].email == email.lower():
            logged_user = server.users[key]
            user_key = key
            break

    if logged_user is -1:
        raise ValueError('Email does not belong to a user')

    # hash the password before storing it so passwords aren't stored in plaintext
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    if hashed_password != logged_user.password:
        raise ValueError('Password is not correct')

    token = server.users[user_key].newToken()

    return {"u_id": logged_user.u_id, "token": token}

# ValueError exception when:
#   Email entered is not a valid email
#   Email entered does not belong to a user
#   Password is not correct


def auth_logout(token):
    '''
    Given an active token, invalidates the taken to log the user out. If a valid
    token is given, and the user is successfully logged out, it returns true,
    otherwise false.
    '''
    if token is None or not isinstance(token, str):
        raise TypeError('Type should be string')

    payload = functions.helper_tokens.tokenPayload(token)
    if not payload:
        return {'is_success': False}

    token_num = payload['tokenNum']
    user_id = payload['u_id']

    try:
        insta_index = server.users[user_id]
        if insta_index.invalidateToken(token_num):
            return {'is_success': True}
    except KeyError:
        pass

    return {'is_success': False} # pragma: no cover


def auth_register(email, password, name_first, name_last):
    '''
    Given a user's first and last name, email address, and password, create a new
    account for them and return a new token for authentication in their session.
    A handle is generated that is the concatentation of a lowercase-only first name
    and last name. If the handle is already taken, a number is added to the end of
    the handle to make it unique.
    '''
    if email is None or not isinstance(email, str):
        raise TypeError('email should be string')
    if password is None or not isinstance(password, str):
        raise TypeError('password should be string')
    if name_first is None or not isinstance(name_first, str):
        raise TypeError('name_first should be string')
    if name_last is None or not isinstance(name_last, str):
        raise TypeError('name_last should be string')

    if not functions.general.emailCheck(email):
        raise ValueError('Email is not valid')

    if len(password) < 6:
        raise ValueError('Password must be greater than 5 characters')
    if len(name_first) > 50 or len(name_first) < 1 or len(name_last) > 50 or len(name_last) < 1:
        raise ValueError('Names must be between 1 and 50 characters')

    for key in server.users:
        if server.users[key].email == email.lower():
            raise ValueError('Email is already being used by another user')

    num = 0
    handle = name_first.lower() + name_last.lower()
    handle = handle[0:20]
    new_handle = handle
    while True:
        for key in server.users:
            if server.users[key].handle == handle:
                if len(name_first.lower() + name_last.lower() + str(num)) > 20:
                    new_handle = handle[0:(20-len(str(num)))]
                else:
                    new_handle = name_first.lower() + name_last.lower()
                new_handle = new_handle + str(num)
                num += 1
                break
        if handle == new_handle:
            break
        handle = new_handle

    u_id = len(server.users) + 1
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    new_user = functions.classes.User(email.lower(), hashed_password,
                                      name_first, name_last, handle, u_id)
    if u_id == 1:
        new_user.permission_id = 1
    token = new_user.newToken()

    if u_id not in server.users.keys():
        server.users[u_id] = new_user
    else:
        raise ValueError('u_id being overwritten?')

    return {"u_id": u_id, "token": token}

# ValueError exception when:
#   email is not a valid email
#   email is being used by another user
#   password is not valid (less than 6 characters)
#   name_first is more than 50 characters or less than 1
#   name_last is more than 50 characters or less than 1


def auth_passwordreset_request(email):
    '''
    Given an email address, if the user is a registered user, send's them a an email
    containing a specific secret code, that when entered in auth_passwordreset_reset,
    shows that the user trying to reset the password is the one who got sent this email.
    '''
    if email is None or not isinstance(email, str):
        raise TypeError("Email must be a string")
    if not functions.general.emailCheck(email):
        return {}

    for key in server.users:
        if email == server.users[key].email:
            name = server.users[key].name_first
            reset_code = code_gen() # assumes each user can only have one reset_code
            try: # pragma: no cover
                mail = Mail(server.APP)
                msg = Message("Password reset request",
                              sender="pycharmers.1531@gmail.com",
                              recipients=[email])
                msg.body = "Hello " + name + ".\nYour reset code is: " + reset_code
                thr = threading.Thread(target=send_mail_flask, args=[msg, mail])
                thr.start()
            except NameError: # Not much point
                # send_mail_mutt(reset_code, email)
                pass
            server.users[key].reset_code = hashlib.sha256(reset_code.encode()).hexdigest()
            break # only 1 user can have a given email
    return {}

def send_mail_flask(msg, mail): # pragma: no cover
    ''' Send an email through flask_mail '''
    with server.APP.app_context():
        mail.send(msg)

def code_gen():
    ''' Generate a random 6 character reset code '''
    # Check that the reset code isn't repeated for now because reset/reset doesn't
    # check the account name = user.name_first, only takes code and new_password
    while True:
        # consider removing characters that look similar
        code = (''.join(random.choices(string.ascii_uppercase+string.digits, k=6))).upper()
        for key in server.users:
            if hasattr(server.users[key], 'reset_code'):
                if getattr(server.users[key],
                           'reset_code') == hashlib.sha256(code.encode()).hexdigest():
                    continue
        return code


def auth_passwordreset_reset(reset_code, new_password):
    '''
    Given a reset code for a user, set that user's new password to the
    password provided
    '''
    if reset_code is None or not isinstance(reset_code, str):
        raise TypeError("reset_code must be str")
    if new_password is None or not isinstance(new_password, str):
        raise TypeError("new_password must be str")

    for key in server.users:
        if len(new_password) < 6:
            raise ValueError("Invalid password")
        if hasattr(server.users[key], 'reset_code'):
            if server.users[key].reset_code == hashlib.sha256(reset_code.encode()).hexdigest():
                del server.users[key].reset_code
                hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
                server.users[key].password = hashed_password
                # because the hashed_password is checked to validateTokens,
                # all previously made tokens should be invalidated
                # to be safe we'll empty the tokenNums for the user
                server.users[key].tokenNums.clear()
                return {}

    raise ValueError("Invalid reset code")

# ValueError exception when:
#   reset_code is not a valid reset code
#   password entered is not a valid password


def admin_userpermission_change(token, u_id, permission_id):
    '''
    Given a User by their user ID, set their permissions to new permissions
    described by permission_id
    '''
    token = functions.errors.check_str(token, 'token')
    u_id = functions.errors.check_int(u_id, 'u_id')
    permission_id = functions.errors.check_int(permission_id, 'u_id')

    permission_changer = functions.helper_tokens.get_user(token)
    permission_changee = functions.helper_users.get_user(u_id)

    if permission_id < 1 or permission_id > 3:
        raise ValueError("Not a valid permission ID")

    if permission_changer.permission_id > permission_changee.permission_id:
        raise functions.errors.AccessError("You do not have permission")
    if permission_changer.permission_id > permission_id:
        raise functions.errors.AccessError("You do not have permission")
    if permission_changer.permission_id == 3:
        raise functions.errors.AccessError("You do not have permission")
    permission_changee.permission_id = permission_id
    return {}

# ValueError exception when:
#   u_id does not refer to a valid user
#   permission_id does not refer to a value permission
# AccessError exception when:
#   The authorised user is not an admin or owner
