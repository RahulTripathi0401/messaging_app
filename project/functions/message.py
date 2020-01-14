'''
Send a message from authorised_user to the channel specified by channel_id
automatically at a specified time in the future
'''
import datetime
from threading import Timer

import functions.helper_channel
import functions.helper_tokens
import functions.errors
import functions.classes
import functions.helper_messages
import server


def message_sendlater(token, channel_id, message, time_sent):
    ''' Given a message, sends it into a given channel at a given time '''
    token = functions.errors.check_str(token, 'token')
    channel_id = functions.errors.check_int(channel_id, 'channel_id')
    message = functions.errors.check_str(message, 'message')
    functions.helper_messages.check_message_length(message)

    user = functions.helper_tokens.get_user(token)
    channel = functions.helper_channel.get_channel(channel_id)
    functions.helper_channel.check_member(channel, user.u_id)

    try:
        time_sent = float(time_sent)
    except ValueError:
        raise TypeError('Time is invalid')

    time_sent = int(time_sent)

    found_channel = None
    try:
        if server.channels[channel_id].channel_id == channel_id:
            found_channel = server.channels[channel_id]
    except KeyError:
        raise ValueError('Channel not found')

    timenow = datetime.datetime.now().timestamp()
    length = (time_sent - timenow)
    if length < 0:
        raise ValueError("time_sent is a time in the past")
    found_channel.messageCount += 1
    m_id = int(str(channel_id) + "000123000" + str(channel.messageCount))
    new_message = functions.classes.Message(m_id, message, user.u_id)
    thread = Timer(length, late_message, [new_message, channel])

    thread.start()

    return {'message_id': m_id}

def late_message(new_message, found_channel):
    ''' Add a message to a channel '''
    new_message.timeCreated = datetime.datetime.now()
    found_channel.messages[new_message.message_id] = new_message

#Send a message from authorised_user to the channel specified by channel_id

def message_send(token, channel_id, message):
    ''' Send a message from authorised_user to the channel specified by channel_id '''
    token = functions.errors.check_str(token, 'token')
    channel_id = functions.errors.check_int(channel_id, 'channel_id')
    message = functions.errors.check_str(message, 'message')
    functions.helper_messages.check_message_length(message)
    #checks user and channel exist and user is channel member
    user = functions.helper_tokens.get_user(token)
    channel = functions.helper_channel.get_channel(channel_id)
    functions.helper_channel.check_member(channel, user.u_id)
    #generates message ID and increments message count in channel
    m_id = int(str(channel_id) + "000123000" + str(channel.messageCount+1))
    channel.messageCount += 1
    #creates new message and adds it to channel messages dictionary
    new_message = functions.classes.Message(m_id, message, user.u_id)
    channel.messages[m_id] = new_message
    return {"message_id": m_id}

#Given a message_id for a message, this message is removed from the channel

def message_remove(token, message_id):
    ''' Remove a given message '''
    token = functions.errors.check_str(token, 'token')
    message_id = functions.errors.check_int(message_id, 'message_id')

    channel_id = int(str(message_id).split("000123000")[0])
    user = functions.helper_tokens.get_user(token)
    channel = functions.helper_channel.get_channel(channel_id)
    functions.helper_channel.check_member(channel, user.u_id)

    # check message_id is valid
    if not functions.helper_messages.message_exists(message_id):
        raise ValueError("Message does not exist")
    # check that user is an authorised member
        # creator of message or owner of channel
    message_creator = functions.helper_messages.message_uid(message_id)
    if message_creator is None:
        raise functions.errors.AccessError("Invalid message?")
    is_user_owner = functions.helper_channel.userIsOwner(user_id=user.u_id, channel_id=channel_id)
    if not message_creator == user.u_id and not is_user_owner:
        raise functions.errors.AccessError("User doesn't have permission to remove message")

    try:
        if server.channels[channel_id].channel_id == channel_id:
            if server.channels[channel_id].messages[message_id].message_id == message_id:
                del server.channels[channel_id].messages[message_id]
                return {}
    except KeyError:
        raise ValueError('Message not found')

    return {}


#Given a message, update it's text with new text

def message_edit(token, message_id, message):
    ''' Edits a given message '''
    token = functions.errors.check_str(token, 'token')
    message_id = functions.errors.check_int(message_id, 'message_id')
    message = functions.errors.check_str(message, 'message')
    functions.helper_messages.check_message_length(message)
    if message == "":
        message_remove(token, message_id)
        return {}

    channel_id = int(str(message_id).split("000123000")[0])

    user = functions.helper_tokens.get_user(token)
    channel = functions.helper_channel.get_channel(channel_id)
    functions.helper_channel.check_member(channel=channel, user_id=user.u_id)

    if not functions.helper_messages.message_exists(message_id):
        raise ValueError("Message does not exist")
    message_creator = functions.helper_messages.message_uid(message_id)
    if message_creator is None:
        raise functions.errors.AccessError("Invalid message?")
    is_user_owner = functions.helper_channel.userIsOwner(user_id=user.u_id, channel_id=channel_id)

    if not message_creator == user.u_id and not is_user_owner:
        raise functions.errors.AccessError("User doesn't have permission to edit message")


    try:
        if channel.channel_id == channel_id:
            if server.channels[channel_id].messages[message_id].message_id == message_id:
                server.channels[channel_id].messages[message_id].message = message
                return {}
    except KeyError:
        raise ValueError("Message not found")

    return {}


#Given a message within a channel the authorised user is part of, add a "react"
#to that particular message


def message_react(token, message_id, react_id):
    ''' Given a message within a channel the authorised user is part of, add a "react"
    to that particular message '''
    token = functions.errors.check_str(token, 'token')
    message_id = functions.errors.check_int(message_id, 'message_id')
    react_id = functions.errors.check_int(react_id, 'react_id')

    channel_id = int(str(message_id).split("000123000")[0])
    functions.errors.check(react_id == 1, 'Invalid react_id')

    user = functions.helper_tokens.get_user(token)
    channel = functions.helper_channel.get_channel(channel_id)
    functions.helper_channel.check_member(channel=channel, user_id=user.u_id)

    if message_id in channel.messages:
        reacts = channel.messages[message_id].reacts
    else:
        raise ValueError("message_id is not a valid message")

    if react_id in reacts:
        if user.u_id in reacts[react_id].u_ids:
            raise ValueError("The message has already been reacted")
        if not user.u_id in reacts[react_id].u_ids:
            reacts[react_id].u_ids.append(user.u_id)
    else:
        reacts[react_id] = functions.classes.React(react_id)
        reacts[react_id].u_ids.append(user.u_id)
    return {}

#Given a message within a channel the authorised user is part of, remove a
#"react" to that particular message

def message_unreact(token, message_id, react_id):
    ''' Given a message within a channel the authorised user is part of, remove a
    "react" to that particular message '''
    token = functions.errors.check_str(token, 'token')
    message_id = functions.errors.check_int(message_id, 'message_id')
    react_id = functions.errors.check_int(react_id, 'react_id')

    channel_id = int(str(message_id).split("000123000")[0])
    functions.errors.check(react_id == 1, 'Invalid react_id')

    user = functions.helper_tokens.get_user(token)
    channel = functions.helper_channel.get_channel(channel_id)
    functions.helper_channel.check_member(channel=channel, user_id=user.u_id)
    message = functions.helper_messages.get_message(m_id=message_id, channel=channel)

    react_exists = False
    reacts = message.reacts
    if react_id in reacts:
        react_exists = True
        if user.u_id not in reacts[react_id].u_ids:
            raise ValueError("The message has already been unreacted")
        if user.u_id in reacts[react_id].u_ids:
            reacts[react_id].u_ids.remove(user.u_id)
    if not react_exists:
        raise ValueError("The message is already unreacted")
    return {}

#Given a message within a channel, mark it as "pinned" to be given special
#display treatment by the frontend

def message_pin(token, message_id):
    ''' Given a message within a channel, mark it as "pinned" to be given special
    display treatment by the frontend '''
    token = functions.errors.check_str(token, 'token')
    message_id = functions.errors.check_int(message_id, 'message_id')
    channel_id = int(str(message_id).split("000123000")[0])

    user = functions.helper_tokens.get_user(token)
    channel = functions.helper_channel.get_channel(channel_id)
    functions.helper_channel.check_member(channel=channel, user_id=user.u_id)

    if not user.is_admin():
        raise ValueError('User does not have permission to edit message')
    message = functions.helper_messages.get_message(m_id=message_id, channel=channel)

    if message.is_pinned:
        raise ValueError("The message is already pinned")
    message.is_pinned = True
    return {}


#Given a message within a channel, remove it's mark as unpinned

def message_unpin(token, message_id):
    ''' Given a message within a channel, remove it's mark as unpinned '''
    token = functions.errors.check_str(token, 'token')
    message_id = functions.errors.check_int(message_id, 'message_id')

    channel_id = int(str(message_id).split("000123000")[0])

    user = functions.helper_tokens.get_user(token)
    channel = functions.helper_channel.get_channel(channel_id)
    functions.helper_channel.check_member(channel=channel, user_id=user.u_id)

    functions.errors.check(user.is_admin(), 'User does not have permission to edit message')
    message = functions.helper_messages.get_message(m_id=message_id, channel=channel)

    if not message.is_pinned:
        raise ValueError('The message is already un-pinned')
    message.is_pinned = False
    return {}
