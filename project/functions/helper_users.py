'''
Assists with user requests
'''
from server import users

def userExists(u_id):
    ''' Return Boolean if a user exists '''
    try:
        if users[u_id].u_id == u_id:
            return True
    except KeyError:
        pass

    return False

def get_user(u_id):
    ''' Return a user object from u_id '''
    if not u_id in users:
        raise ValueError("Not a slackr user")
    return users[u_id]
