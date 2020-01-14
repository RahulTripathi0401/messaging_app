''' Pytests written to test the 'functions.message.message_sendlater' function '''
import time
from datetime import datetime
import pytest
import functions.general
import functions.errors
import functions.message
import functions.auth_functions
import functions.channel
import functions.helper_tokens

def test_message():
    functions.general.clearDatabase()
    long_message = "a" * 1001
    with pytest.raises(ValueError):
        functions.message.message_sendlater("token", 1, long_message, datetime.now())

def test_channelid_invalid():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    with pytest.raises(ValueError):
        functions.message.message_sendlater(bob_info['token'], -1, "message", datetime.now())

def test_message_in_past():
    functions.general.clearDatabase()
    past_time = int(datetime.now().timestamp())
    past_time -= 3
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    token = bob_info['token']
    channelid = functions.channel.channels_create(token, "Bob", True)
    with pytest.raises(ValueError):
        functions.message.message_sendlater(token, channelid['channel_id'], "message", past_time)

def test_general():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    token = bob_info['token']
    channelid = functions.channel.channels_create(bob_info['token'], "name", True)
    chid = channelid['channel_id']
    future = int(datetime.now().timestamp())
    future += 5
    path = functions.channel
    assert path.channel_messages(token, chid, 0) == {'messages': [], 'start': 0, 'end': -1}
    path = functions.message
    assert path.message_sendlater(token, chid, "hello", future) == {'message_id': 10001230001}
    time.sleep(5)
    message = functions.channel.channel_messages(bob_info['token'], chid, 0)
    assert message['messages'][0]['message'] == 'hello'
    assert message['messages'][0]['message_id'] == 10001230001
    assert abs(message['messages'][0]['time_created'] - future) < 2

def test_wrong_token_type():
    functions.general.clearDatabase()
    with pytest.raises(TypeError):
        functions.message.message_sendlater(123, 1, "hello", datetime.now().timestamp())

def test_wrong_channel_id_type():
    functions.general.clearDatabase()
    with pytest.raises(TypeError):
        functions.message.message_sendlater("token", "chid", "hello", datetime.now().timestamp())

def test_wrong_message_type():
    functions.general.clearDatabase()
    with pytest.raises(TypeError):
        functions.message.message_sendlater("token", 1, 123, datetime.now().timestamp())

def test_wrong_time_sent_type():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    functions.channel.channels_create(bob_info['token'], "Bob", True)
    with pytest.raises(TypeError):
        functions.message.message_sendlater(bob_info['token'], 1, "hello", "date")

def test_invalid_token():
    functions.general.clearDatabase()
    with pytest.raises(functions.errors.AccessError):
        functions.message.message_sendlater("token", 1, "hello", datetime.now().timestamp())

def test_user_not_in_channel():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    token = bob_info['token']
    channel = functions.channel.channels_create(bob_info['token'], "Bob", True)
    chid = channel['channel_id']
    functions.channel.channel_leave(bob_info['token'], channel['channel_id'])
    with pytest.raises(functions.errors.AccessError):
        functions.message.message_sendlater(token, chid, "hello", datetime.now().timestamp())

def test_no_channel():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    token = bob_info['token']
    functions.channel.channels_create(token, "Bob", True)
    with pytest.raises(ValueError):
        functions.message.message_sendlater(token, 2, "hello", datetime.now().timestamp())
