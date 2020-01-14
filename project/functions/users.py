'''
All user functions
'''
### For a valid user, returns information about their email, first name, last name, and handle

import urllib.request
import string
import random
import mimetypes
import glob
import requests
from PIL import Image

import functions.helper_users
import functions.general
import functions.helper_tokens
import functions.classes
import functions.errors

import server

def user_profile(token, u_id):
    token = functions.errors.check_str(token, 'token')
    u_id = functions.errors.check_int(u_id, 'u_id')

    user = functions.helper_tokens.get_user(token)

    if not u_id in server.users:
        raise ValueError("User with u_id is not a valid user")
    user = server.users[u_id]
    return user.getUserDict()
# ValueError exception when:
#   User with u_id is not a valid user

### Update the authorised user's first and last name

def user_profile_setname(token, name_first, name_last):
    name_first = functions.errors.check_str(name_first, 'name_first')
    name_last = functions.errors.check_str(name_last, 'name_last')
    token = functions.errors.check_str(token, 'token')

    user = functions.helper_tokens.get_user(token)

    if len(name_first) > 50 or len(name_first) < 1 or len(name_last) > 50 or len(name_last) < 1:
        raise ValueError('Names must be between 1 and 50 characters')

    user.name_first = name_first
    user.name_last = name_last
    return {}

# ValueError exception when:
#   name_first is more than 50 characters
#   name_last is more than 50 characters

### Update the authorised user's email address

def user_profile_setemail(token, email):
    token = functions.errors.check_str(token, 'token')
    email = functions.errors.check_str(email, 'email')
    user = functions.helper_tokens.get_user(token)

    if not functions.general.emailCheck(email):
        raise ValueError('Email is not valid')
    for u_id in server.users:
        if server.users[u_id].email == email:
            raise ValueError("The email is already used")

    user.email = email.lower()
    return {}

# ValueError exception when:
#   Email entered is not a valid email.
#   Email address is already being used by another user

### Update the authorised user's handle (i.e. display name)

def user_profile_sethandle(token, handle_str):
    token = functions.errors.check_str(token, 'token')
    handle_str = functions.errors.check_str(handle_str, 'email')

    user = functions.helper_tokens.get_user(token)
    if len(handle_str) > 20:
        raise ValueError("Handle must not be more than 20 characters long")

    user.handle = handle_str
    return {}


### Given a URL of an image on the internet, crops the image within bounds
### (x_start, y_start) and (x_end, y_end). Position (0,0) is the top left.

def user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end, y_end): # pragma: no cover
    ''' Change the photo of a user '''
    if not functions.helper_tokens.tokenValidity(token):
        raise functions.errors.AccessError("Token is invalid")
    try:
        x_start = int(x_start)
        y_start = int(y_start)
        x_end = int(x_end)
        y_end = int(y_end)
    except ValueError:
        raise TypeError("Coords should be integers")

    try:
        response = requests.get(img_url)
        content_type = response.headers['content-type']
        extension = mimetypes.guess_extension(content_type)
    except requests.exceptions.ConnectionError:
        raise ValueError("Please provide a valid URL")

    if extension is None or extension == '.jpe':
        extension = ".jpg"

    # Could make it a hash so you don't end up with duplicates
    while True:
        name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        if not glob.glob("static/name.*"):
            break

    urllib.request.urlretrieve(img_url, "static/"+name+extension)

    try:
        image_object = Image.open("static/"+name+extension)
    except OSError:
        raise ValueError("Please provide a valid image URL")

    try:
        cropped = image_object.crop((x_start, y_start, x_end, y_end))
        cropped.save("static/"+name+extension)
    except SystemError:
        raise ValueError("Please provide valid coords")

    server.users[functions.helper_tokens.token_u_id(token)].profile_img_url = \
    "/static/" + name + extension

    return {}

# ValueError exception when:
#   img_url is returns an HTTP status other than 200.
#   x_start, y_start, x_end, y_end are all within the dimensions of the image at the URL.
        # ? probably opposite

### Return a list of all users in the slackr

def users_all(token):
    '''' Given a token, return a list of all users '''
    token = functions.errors.check_str(token, 'token')
    user = functions.helper_tokens.get_user(token)
    user_return = []
    for key in server.users:
        user_return.append(server.users[key].getUserDict())

    return {'users': user_return}
