'''
Helper functions that assist channel calls
'''
from server import users, channels
import functions.errors

def channelExists(channel_id):
    ''' Check if a channel exists '''
    try:
        if channels[channel_id].channel_id == channel_id:
            return True
    except KeyError:
        pass

    return False

def userInChannel(channel_id, u_id):
    ''' Check if a user is in a channel '''
    try:
        if channels[channel_id].channel_id == channel_id:
            return channels[channel_id].isMember(u_id)
    except KeyError:
        pass

    return False

def addUserToChannel(channel_id, u_id):
    ''' Add a user to a channel '''
    try:
        if channels[channel_id].channel_id == channel_id:
            if users[u_id].u_id == u_id:
                channels[channel_id].members[u_id] = users[u_id].getDict()
                return
    except KeyError:
        pass

    return

def userIsOwner(user_id, channel_id):
    ''' Check if a user is an owner of a channel '''
    try:
        if channels[channel_id].channel_id == channel_id:
            return channels[channel_id].isOwner(user_id)
    except KeyError:
        pass

    return False

# Returns the channel for the given channel id.
# raises ValueError if the channel does not exist
def get_channel(channel_id):
    ''' Return the channel object from a channel_id '''
    if channel_id not in channels:
        raise ValueError('Invalid channel')
    return channels[channel_id]

# raises AccessError if the user associated with the given user id is not
# a member of the channel
def check_member(channel, user_id):
    ''' Raise an error if a user is not a member of a channel '''
    if not channel.isMember(user_id):
        raise functions.errors.AccessError('Not a channel member')

def check_not_member(channel, user_id):
    ''' Raise an error if a user is already a member of a channel '''
    if channel.isMember(user_id):
        raise functions.errors.AccessError('Already channel member')
