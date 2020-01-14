'''
Helper messages to assist with message function call
'''
from server import channels

def message_uid(message_id):
    ''' Get the u_id of the sender of a message '''
    channel_id = int(str(message_id).split("000123000")[0])

    try:
        if channels[channel_id].channel_id == channel_id:
            try:
                if channels[channel_id].messages[message_id].message_id == message_id:
                    return channels[channel_id].messages[message_id].sender
            except KeyError:
                pass
    except KeyError:
        pass

    return None

def message_exists(message_id):
    ''' Check that a message_id refers to an existing message '''
    channel_id = int(str(message_id).split("000123000")[0])

    try:
        if channels[channel_id].channel_id == channel_id:
            try:
                if channels[channel_id].messages[message_id].message_id == message_id:
                    return True
            except KeyError:
                pass
    except KeyError:
        pass

    return False

def get_message(m_id, channel):
    ''' Get the message objet from a message id '''
    if m_id not in channel.messages:
        raise ValueError('message_id is not a valid message')
    return channel.messages[m_id]

def check_message_length(message):
    ''' Check the length of a message '''
    if len(message) > 1000:
        raise ValueError('Message longer than 1000 characters')
