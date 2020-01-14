''' Pytests written to test the 'functions.message.message_edit' function '''
import pytest
import functions.general
import functions.errors
import functions.message
import functions.auth_functions
import functions.channel
import functions.helper_tokens

def test_edit_wrong_user():
    functions.general.clearDatabase()
    with pytest.raises(functions.errors.AccessError):
        functions.message.message_edit("Invalid token", 10001230001, "hello and hi")

def test_message_edit_invalid_user():
    functions.general.clearDatabase()
    with pytest.raises(TypeError):
        functions.message.message_edit(12345, 10001230001, "hello and hi")

# owner editing someone elses message
def test_message_edit_by_owner():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    channelid = functions.channel.channels_create(bob_info['token'], "name", True)
    tom_info = functions.auth_functions.auth_register("tom@email.com", "password", "Tom", "Best")
    functions.channel.channel_join(tom_info['token'], channelid['channel_id'])
    mid = functions.message.message_send(tom_info['token'], channelid['channel_id'], "Test")
    token = bob_info['token']
    ch_id = channelid['channel_id']
    assert functions.channel.channel_messages(token, ch_id, 0)['messages'][0]['message'] == "Test"
    functions.message.message_edit(bob_info['token'], mid['message_id'], "hi")
    assert functions.channel.channel_messages(token, ch_id, 0)['messages'][0]['message'] == "hi"

# editing a message you dont have permission for
def test_message_edit_by_wrong():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    channelid = functions.channel.channels_create(bob_info['token'], "name", True)
    mid = functions.message.message_send(bob_info['token'], channelid['channel_id'], "Test message")
    tom_info = functions.auth_functions.auth_register("tom@email.com", "password", "Tom", "Best")
    functions.channel.channel_join(tom_info['token'], channelid['channel_id'])
    with pytest.raises(functions.errors.AccessError):
        functions.message.message_edit(tom_info['token'], mid['message_id'], "hello and hi")

# editing a message while not in the channel
def test_message_edit_outside():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    token = bob_info['token']
    channelid = functions.channel.channels_create(token, "Pycharmers", True)['channel_id']
    mid = functions.message.message_send(bob_info['token'], channelid, "this is a message")
    functions.channel.channel_leave(bob_info['token'], channelid)
    with pytest.raises(functions.errors.AccessError):
        functions.message.message_edit(bob_info['token'], mid['message_id'], "hello and hi")


def test_message_edit_simple():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    token = bob_info['token']
    channelid = functions.channel.channels_create(token, "Pycharmers", True)['channel_id']
    functions.message.message_send(bob_info['token'], channelid, "this is a message")
    message = functions.channel.channel_messages(bob_info['token'], channelid, 0)
    assert message['messages'][0]['message'] == 'this is a message'
    functions.message.message_edit(token, message['messages'][0]['message_id'], "hello and hi")
    message = functions.channel.channel_messages(bob_info['token'], channelid, 0)
    assert message['messages'][0]['message'] == 'hello and hi'

def test_wrong_message_id_type():
    functions.general.clearDatabase()
    with pytest.raises(TypeError):
        functions.message.message_edit("token", "mid", "hello and hi")

def test_wrong_message_type():
    functions.general.clearDatabase()
    with pytest.raises(TypeError):
        functions.message.message_edit("token", 1, 1)

def test_long_message():
    functions.general.clearDatabase()
    with pytest.raises(ValueError):
        functions.message.message_edit("token", 1, "a" * 1001)

def test_fake_channel():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    with pytest.raises(ValueError):
        functions.message.message_edit(bob_info['token'], 70001230001, "message")

def test_fake_message():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    channel = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)
    functions.message.message_send(bob_info['token'], channel['channel_id'], "test")
    with pytest.raises(ValueError):
        functions.message.message_edit(bob_info['token'], 10001230002, "message")


def test_remove_empty_string():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    token = bob_info['token']
    channelid = functions.channel.channels_create(token, "Pycharmers", True)['channel_id']
    functions.message.message_send(bob_info['token'], channelid, "this is a message")
    message = functions.channel.channel_messages(bob_info['token'], channelid, 0)
    assert message['messages'][0]['message'] == 'this is a message'
    functions.message.message_edit(bob_info['token'], message['messages'][0]['message_id'], "")
    message = functions.channel.channel_messages(bob_info['token'], channelid, 0)
    assert message['messages'] == []
