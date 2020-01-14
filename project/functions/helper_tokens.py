''' Helper functions for working with tokens '''
import jwt
from server import users
import functions.errors

# Should decide whether all of these should be checking validity or just giving info regardless

def tokenInfo(token):
    ''' Return a user object from a token '''
    if tokenValidity(token):
        payload = jwt.decode(token, "secret", algorithms=['HS256'],
                             options={'verify_signature': False})
        user_id = payload['u_id']
        try:
            return users[user_id]
        except KeyError:
            return False
    return False


# # Return a boolean signifying whether a given token is valid or not
#     # used by auth_login_test, auth_logout_test, auth_register_test
def tokenValidity(token):
    ''' Boolean return whether a token is valid or not '''
    try:
        payload = jwt.decode(token, "secret", algorithms=['HS256'],
                             options={'verify_signature': False})
    except jwt.exceptions.DecodeError:
        return False
    user_id = payload['u_id']

    insta_index = None

    try:
        insta_index = users[user_id]
    except KeyError:
        pass

    if insta_index is not None:
        if insta_index.u_id == user_id:
            if payload['tokenNum'] in insta_index.tokenNums:
                try:
                    # just checking to make sure signature is valid too
                    jwt.decode(token, insta_index.password, algorithms=['HS256'])
                    return True
                except jwt.exceptions.InvalidSignatureError:
                    pass

    return False

# # Return the email address associated with the user associated with a given token
#     # used by auth_login_test, auth_register_test
def tokenEmail(token):
    ''' Return the email of a user associated with a given token '''
    if tokenValidity(token):
        payload = jwt.decode(token, "secret", algorithms=['HS256'],
                             options={'verify_signature': False})
        user_id = payload['u_id']
        insta_index = users[user_id]
        if insta_index.u_id == user_id:
            return insta_index.email
    return None

# If a token is valid, return the payload
def tokenPayload(token):
    ''' Return the payload from a token if the token is valid '''
    if tokenValidity(token):
        return jwt.decode(token, "secret", algorithms=['HS256'],
                          options={'verify_signature': False})
    return False

# # Return the u_id associated with the user associated with a given token
#     # used by auth_login_test, auth_register_test
def token_u_id(token):
    ''' Return the u_id of a token '''
    if tokenValidity(token):
        payload = jwt.decode(token, "secret", algorithms=['HS256'],
                             options={'verify_signature': False})
        return payload['u_id']
    return None

# Returns the user associated with a given token.
# raises AccessError if the token is invalid
# raises ValueError if the token is not for a slackr user
def get_user(token):
    ''' Return the user from a token '''
    u_id = token_u_id(token)
    if u_id is None:
        raise functions.errors.AccessError('Invalid token')
    if not u_id in users:
        raise ValueError("Not a slackr user")
    return users[u_id]

# # Return a tuple with the first and last names of the user associated with a given token
#     # used by auth_register_test
def tokenNames(token):
    ''' Return a tuple of a user associated with a token '''
    if tokenValidity(token):
        payload = jwt.decode(token, "secret", algorithms=['HS256'],
                             options={'verify_signature': False})
        user_id = payload['u_id']
        insta_index = users[user_id]
        if insta_index.u_id == user_id:
            return (insta_index.name_first, insta_index.name_last)
    return None

# Return the handle associated with the user of a given token
def tokenHandle(token):
    ''' Return the handle of a user associated with a token '''
    payload = tokenPayload(token)
    if not payload:
        return False
    user_id = payload['u_id']
    token_user = users[user_id]
    return token_user.handle

# # Return the url of the profile image of the user associated with a given token
#     # used by user_profiles_uploadphoto_test
# def token_image(token):
#     return "https://exampleimage.com"
