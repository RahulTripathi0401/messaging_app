''' functions for standups'''
from datetime import timedelta

import functions.general as general
import functions.helper_tokens
import functions.helper_messages
import functions.errors
import functions.message
import server


def standup_finish(token, channel):
    ''' Actions taken once a standup is complete '''
    message = '\n'.join(map(str, channel.standup_messages))
    functions.message.message_send(token, channel.channel_id, message)
    channel.standup_timer = None
    channel.standup_length = None
    channel.standup_endtime = None
    channel.standup_messages = []


# For a given channel, start the standup period whereby for the next 15 minutes
# if someone calls "standup_send" with a message, it is buffered during the
# 15 minute window then at the end of the 15 minute window a message will be
# added to the message queue in the channel from the user who started the standup.
# ValueError exception when:
#   Channel (based on ID) does not exist
# functions.errors.AccessError exception when:
#   The authorised user is not a member of the channel that the message is within
def standup_start(token, channel_id, length):
    ''' Starting a standup period '''
    token = functions.errors.check_str(token, 'token')
    channel_id = functions.errors.check_int(channel_id, 'channel_id')
    length = functions.errors.check_int(length, 'length')

    user = functions.helper_tokens.get_user(token)
    channel = functions.helper_channel.get_channel(channel_id)
    functions.helper_channel.check_member(channel, user.u_id)
    functions.errors.check(channel.standup_timer is None,
                           'Standup is already running')

    now = general.get_time()

    channel.standup_timer = now
    channel.standup_messages = []
    channel.standup_length = length
    general.run_later(length, standup_finish, [token, channel])

    time_fin = now+timedelta(minutes=(length/60))
    time_fin = time_fin.timestamp()
    channel.standup_endtime = time_fin
    return {'time_finish': time_fin}


# Sending a message to get buffered in the standup queue, assuming a standup is
# currently active
# raises ValueError exception when:
#   Channel (based on ID) does not exist
#   Message is more than 1000 characters
# raises functions.errors.AccessError exception when:
#   The authorised user is not a member of the channel that the message is within
#   If the standup time has stopped
def standup_send(token, channel_id, message):
    ''' Sending messages into a standup '''
    token = functions.errors.check_str(token, 'token')
    channel_id = functions.errors.check_int(channel_id, 'channel_id')
    message = functions.errors.check_str(message, 'message')
    functions.helper_messages.check_message_length(message)

    user = functions.helper_tokens.get_user(token)
    channel = functions.helper_channel.get_channel(channel_id)
    functions.helper_channel.check_member(channel, user.u_id)
    functions.errors.check(channel.standup_timer is not None,
                           'Standup is not running')

    now = general.get_time()
    standup_finished = (now - channel.standup_timer).total_seconds() \
        < channel.standup_length
    functions.errors.check(standup_finished, 'Standup has finished')
    message = functions.helper_tokens.tokenHandle(token) + ": " + message
    channel.standup_messages.append(message)
    return {}


# For a given channel, return whether a standup is active in it, and what time the
# standup finishes. If no standup is active, then time_finish returns None
# raises ValueError exception when:
#   Channel (based on ID) does not exist
def standup_active(token, channel_id):
    ''' Check if a standup is active '''
    if token is None or not isinstance(token, str):
        raise TypeError('Token should be string')
    if channel_id is None or (not isinstance(channel_id, int) and not channel_id.isdigit()):
        raise TypeError('Channel id not integer')

    user_id = functions.helper_tokens.token_u_id(token)
    if not user_id:
        raise functions.errors.AccessError('Invalid token')
    channel_id = int(channel_id)

    try:
        if not server.channels[channel_id].isMember(user_id):
            raise functions.errors.AccessError('Not a member of this channel')
    except KeyError:
        raise ValueError('Invalid channel')

    if server.channels[channel_id].standup_timer is None:
        is_active = False
        time_finish = None
    else:
        is_active = True
        time_finish = server.channels[channel_id].standup_endtime

    return {'is_active': is_active, 'time_finish': time_finish}
