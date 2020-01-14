'''
Functions called through the channel routes
'''

import functions.errors
import functions.helper_tokens
import functions.helper_channel
import functions.helper_users
import functions.classes
import server

def channel_invite(token, channel_id, u_id):
    '''
    Invites a user (with user id u_id) to join a channel with ID channel_id.
    Once invited the user is added to the channel immediately
    '''
    if token is None or not isinstance(token, str):
        raise TypeError('Token should be string')
    if channel_id is None or (not isinstance(channel_id, int) and not channel_id.isdigit()):
        raise TypeError('Channel id not integer')
    if u_id is None or (not isinstance(u_id, int) and not u_id.isdigit()):
        raise TypeError('u_id not integer')

    channel_id = int(channel_id)
    u_id = int(u_id)

    user_id = functions.helper_tokens.token_u_id(token)
    if user_id is None:
        raise functions.errors.AccessError("Invalid token")
    if not functions.helper_channel.channelExists(channel_id):
        raise ValueError("Channel does not exist")
    if not functions.helper_channel.userInChannel(channel_id, user_id):
        raise ValueError("Authorised user is not a member of the channel")
    if not functions.helper_users.userExists(u_id):
        raise ValueError("User does not exist")
    if functions.helper_channel.userInChannel(channel_id, u_id):
        raise ValueError("User is already a part of the channel")

    functions.helper_channel.addUserToChannel(channel_id, u_id)

    try:
        if server.channels[channel_id].channel_id == channel_id:
            if user_id == server.channels[channel_id].creator:
                if server.users[u_id].u_id == u_id:
                    server.channels[channel_id].owners[u_id] = server.users[u_id].getDict()
                    return {}
    except KeyError:
        raise ValueError('Invalid channel')

    return {}

# ValueError exception when:
#   channel_id does not refer to a valid channel that the authorised user is part of.
#   u_id does not refer to a valid user


def channel_details(token, channel_id):
    '''
    Given a Channel with ID channel_id that the authorised user is part of,
    provide basic details about the channel
    '''
    if token is None or not isinstance(token, str):
        raise TypeError("Token should be a str")

    if channel_id is None or (not isinstance(channel_id, int) and not channel_id.isdigit()):
        raise TypeError("channel_id should be a int")

    channel_id = int(channel_id)

    user = functions.helper_tokens.tokenInfo(token)
    if not user:
        raise functions.errors.AccessError("Invalid token")

    try:
        channel_object = server.channels[channel_id]
    except KeyError:
        raise ValueError("Channel (based on ID) does not exist")

    if channel_object.isMember(user.u_id):
        name = channel_object.name
        owner_members = [server.users[key].getDict() for key in channel_object.owners.keys()]
        all_members = [server.users[key].getDict() for key in channel_object.members.keys()]
    else:
        raise functions.errors.AccessError("Authorised user is not a member of \
                                            channel with channel_id")

    return {"name": name,
            "owner_members": owner_members,
            "all_members": all_members}

# ValueError exception when:
#   Channel (based on ID) does not exist
# functions.errors.AccessError exception when:
#   Authorised user is not a member of channel with channel_id


def channel_messages(token, channel_id, start):
    '''
    Given a Channel with ID channel_id that the authorised user is part of,
    return up to 50 messages between index "start" and "start + 50".
    Message with index 0 is the most recent message in the channel.
    This function returns a new index "end" which is the value of "start + 50", or,
    if this function has returned the least recent messages in the channel, returns
    -1 to indicate there are no more messages to load after this return.
    '''
    token = functions.errors.check_str(token, 'token')
    channel_id = functions.errors.check_int(channel_id, 'channel_id')
    start = functions.errors.check_int(start, "start")

    user = functions.helper_tokens.get_user(token)
    channel = functions.helper_channel.get_channel(channel_id)
    functions.helper_channel.check_member(channel, user.u_id)

    if start == 0 and len(channel.messages) == 0:
        return {"messages": [], "start": start, "end": -1}

    functions.errors.check(start < len(channel.messages), 'Channel contains fewer \
                                                           messages than that')

    end = start + 50
    #order message dictionary of objects as list of most recently created
    messages = list(reversed(sorted(channel.messages.values(), key=lambda m: m.timeCreated)))
    if len(messages) < end:
        messages = messages[start:]
        end = -1
    else:
        messages = messages[start:end]
    #convert list of objects into list of dictionaries
    messages = [message.getDict(user.u_id) for message in messages]
    return {"messages": messages, "start": start, "end": end}

# ValueError exception when:
#   Channel (based on ID) does not exist
#   start is greater than the total number of messages in the channel
# functions.errors.AccessError exception when:
#   Authorised user is not a member of channel with channel_id


def channel_leave(token, channel_id):
    '''
    Given a channel ID, the user removed as a member of this channel
    '''
    token = functions.errors.check_str(token, 'token')
    channel_id = functions.errors.check_int(channel_id, 'channel_id')

    user = functions.helper_tokens.get_user(token)
    channel = functions.helper_channel.get_channel(channel_id)
    functions.helper_channel.check_member(channel, user.u_id)

    channel.members.pop(user.u_id, None)
    channel.owners.pop(user.u_id, None)
    return {}

# ValueError exception when:
#   Channel (based on ID) does not exist


def channel_join(token, channel_id):
    '''
    Given a channel_id of a channel that the authorised user can join, adds them
    to that channel
    '''
    token = functions.errors.check_str(token, 'token')
    channel_id = functions.errors.check_int(channel_id, 'channel_id')
    #checks user and channel exist and user is not a channel member
    user = functions.helper_tokens.get_user(token)
    channel = functions.helper_channel.get_channel(channel_id)
    functions.helper_channel.check_not_member(channel, user.u_id)
    # checks channel is not private or user is admin
    if not channel.is_public and not user.is_admin():
        raise functions.errors.AccessError('Private channel')
    # adds user to channel member list
    new_user = user.getDict()
    channel.members[user.u_id] = new_user
    return {}

# ValueError exception when:
#   Channel (based on ID) does not exist
# functions.errors.AccessError exception when:
#   channel_id refers to a channel that is private (when the authorised user is not an admin)


def channel_addowner(token, channel_id, u_id):
    '''
    Make user with user id u_id an owner of this channel
    '''
    if token is None or not isinstance(token, str):
        raise TypeError("Token should be a str")

    if channel_id is None or (not isinstance(channel_id, int) and not channel_id.isdigit()):
        raise TypeError("channel_id should be a int")

    if u_id is None or (not isinstance(u_id, int) and not u_id.isdigit()):
        raise TypeError("u_id should be a int")

    user = functions.helper_tokens.tokenInfo(token)
    if not user:
        raise functions.errors.AccessError("Invalid token")

    channel_id = int(channel_id)
    u_id = int(u_id)

    try:
        channel_object = server.channels[channel_id]
    except KeyError:
        raise ValueError("Channel (based on ID) does not exist")

    user = functions.helper_tokens.token_u_id(token)
    if not functions.helper_channel.userIsOwner(user, channel_id):
        raise functions.errors.AccessError("User is not owner")

    try:
        user_object = server.users[u_id]
    except KeyError:
        raise ValueError("User (based on ID) does not exist")

    if channel_object.isMember(u_id):
        if not channel_object.isOwner(u_id):
            channel_object.owners[u_id] = user_object.getDict()
        else:
            raise ValueError("User is already an owner of the channel")
    else:
        raise functions.errors.AccessError("Authorised user is not a member of \
                                            channel with channel_id")

    return {}

# ValueError exception when:
#   Channel (based on ID) does not exist
#   When user with user id u_id is already an owner of the channel
# functions.errors.AccessError exception when:
#   the authorised user is not an owner of the slackr, or an owner of this channel


def channel_removeowner(token, channel_id, u_id):
    '''
    Remove user with user id u_id an owner of this channel
    '''
    if token is None or not isinstance(token, str):
        raise TypeError("Token should be a str")
    if channel_id is None or (not isinstance(channel_id, int) and not channel_id.isdigit()):
        raise TypeError("channel_id should be a int")
    if u_id is None or (not isinstance(u_id, int) and not u_id.isdigit()):
        raise TypeError("u_id should be a int")
    if u_id < 0:
        raise ValueError("Invalid u_id")
    channel_id = int(channel_id)
    u_id = int(u_id)
    user = functions.helper_tokens.tokenInfo(token)
    if not user:
        raise functions.errors.AccessError("Invalid token")

    try:
        channel_object = server.channels[channel_id]
    except KeyError:
        raise ValueError("Channel (based on ID) does not exist")

    user = functions.helper_tokens.token_u_id(token)
    if not functions.helper_channel.userIsOwner(user, channel_id):
        raise functions.errors.AccessError("User is not owner")

    if not server.channels[channel_id].isMember(u_id):
        raise functions.errors.AccessError("User is not a member of the channel")

    if channel_object.isMember(u_id):
        if channel_object.isOwner(u_id):
            del channel_object.owners[u_id]
        else:
            raise ValueError("User is not owner of the channel")
    else:
        raise functions.errors.AccessError("Authorised user is not a member of \
                                            channel with channel_id")

    return {}

# ValueError exception when:
#   Channel (based on ID) does not exist
#   When user with user id u_id is not an owner of the channel
# functions.errors.AccessError exception when:
#   the authorised user is not an owner of the slackr, or an owner of this channel


def channels_list(token):
    '''
    Provide a list of all channels (and their associated details) that the
    authorised user is part of
    '''
    if token is None or not isinstance(token, str):
        raise TypeError("Token should be a str")

    user = functions.helper_tokens.tokenInfo(token)
    if not user:
        raise functions.errors.AccessError("Invalid token")

    list_return = []

    for channel_key in server.channels:
        if user.u_id in server.channels[channel_key].members.keys():
            list_return.append({'channel_id': server.channels[channel_key].channel_id,
                                'name': server.channels[channel_key].name})

    return {"channels": list_return}


def channels_listall(token):
    '''
    Provide a list of all channels (and their associated details)
    '''
    if token is None or not isinstance(token, str):
        raise TypeError("Token must be a str")

    user = functions.helper_tokens.tokenInfo(token)
    if not user:
        raise functions.errors.AccessError("Invalid token")

    list_return = []

    for channel_key in server.channels:
        if server.channels[channel_key].is_public:
            list_return.append({'channel_id': server.channels[channel_key].channel_id,
                                'name': server.channels[channel_key].name})

    return {"channels": list_return}


def channels_create(token, name, is_public):
    '''
    Creates a new channel with that name that is either a public or private channel
    '''
    if token is None or name is None or is_public is None:
        raise TypeError('missing param')
    if isinstance(is_public, bool):
        pass
    elif not isinstance(is_public, str):
        raise TypeError('is_public should be a boolean')
    elif is_public.lower() == "false":
        is_public = False
    elif is_public.lower() == "true":
        is_public = True
    else:
        raise TypeError("is_public must be a boolean")

    if not isinstance(token, str) or not isinstance(name, str) or not isinstance(is_public, bool):
        raise TypeError("Wrong types")

    if len(name) > 20:
        raise ValueError("Channel name must not be more than 20 characters long")

    user = functions.helper_tokens.tokenInfo(token)
    if not user:
        raise functions.errors.AccessError("Invalid token")

    owner = user.getDict()

    channel_id = len(server.channels) + 1
    new_channel = functions.classes.Channel(channel_id, name, is_public, owner)
    for key in server.users:
        if server.users[key].u_id == user.u_id:
            continue
        if server.users[key].permission_id == 1 or server.users[key].permission_id == 2:
            member_dict = server.users[key].getDict()
            member_u_id = member_dict['u_id']
            new_channel.owners[member_u_id] = member_dict
            new_channel.members[member_u_id] = member_dict

    if channel_id not in server.channels.keys():
        server.channels[channel_id] = new_channel
    else:
        raise ValueError('channel_id being overwritten?')

    return {"channel_id": channel_id}

# ValueError exception when:
#   Name is more than 20 characters long


def search(token, query_str):
    '''
    Given a query string, return a collection of messages that match the query
    '''
    if token is None or not isinstance(token, str):
        raise TypeError('Token should be string')
    if query_str is None or not isinstance(query_str, str):
        raise TypeError('Query should be string')
    user_id = functions.helper_tokens.token_u_id(token)
    if not user_id:
        raise functions.errors.AccessError('Invalid token')
    if len(query_str) > 100:
        raise ValueError('Query string too long')
    messages = []
    for channel in server.channels.values():
        if channel.isMember(user_id):
            for message in channel.messages.values():
                if query_str.lower() in message.message.lower():
                    messages.append(message.getDict(user_id))
    return {'messages': messages}
