'''
Given a message within a channel, mark it as "pinned" to be given special
display treatment by the frontend
'''
import pytest
import functions.general
import functions.errors
import functions.message
import functions.auth_functions
import functions.channel
import functions.helper_tokens

def test_not_valid_message_id():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)
    with pytest.raises(ValueError):
        functions.message.message_pin(bob_info["token"], 10001230005)

def test_general():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    token = bob_info['token']
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)
    message_id = functions.message.message_send(token, channel_id['channel_id'], "hello")
    functions.message.message_pin(bob_info['token'], message_id['message_id'])
    messages = functions.channel.channel_messages(bob_info['token'], channel_id['channel_id'], 0)
    assert messages['messages'][0]['is_pinned']

def test_already_pinned():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    token = bob_info['token']
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)
    message_id = functions.message.message_send(token, channel_id['channel_id'], "hello")
    functions.message.message_pin(bob_info['token'], message_id['message_id'])
    messages = functions.channel.channel_messages(bob_info['token'], channel_id['channel_id'], 0)
    assert messages['messages'][0]['is_pinned']
    with pytest.raises(ValueError):
        functions.message.message_pin(bob_info['token'], message_id['message_id'])

def test_no_admin():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    token = bob_info['token']
    rahul = functions.auth_functions.auth_register("rahul@gmail.com", "password", "rahul", "Test")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)
    functions.channel.channel_join(rahul['token'], channel_id['channel_id'])
    message_id = functions.message.message_send(token, channel_id['channel_id'], "hello")
    functions.message.message_pin(token, message_id['message_id'])
    with pytest.raises(ValueError):
        functions.message.message_pin(rahul['token'], message_id['message_id'])

def test_no_user():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    token = bob_info['token']
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)
    message_id = functions.message.message_send(token, channel_id['channel_id'], "hello")
    functions.channel.channel_leave(bob_info['token'], channel_id['channel_id'])
    with pytest.raises(functions.errors.AccessError):
        assert functions.message.message_pin(bob_info['token'], message_id['message_id']) == {}

def test_token_string():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    token = bob_info['token']
    channel_id = functions.channel.channels_create(token, "Pycharmers", True)
    message_id = functions.message.message_send(token, channel_id['channel_id'], "hello")
    with pytest.raises(TypeError):
        functions.message.message_pin(123, message_id['message_id'])

def test_message_int():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    with pytest.raises(TypeError):
        functions.message.message_pin(bob_info['token'], "hello")

def test_invalid_uid():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    token = bob_info['token']
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)
    message_id = functions.message.message_send(token, channel_id['channel_id'], "hello")
    with pytest.raises(functions.errors.AccessError):
        functions.message.message_pin("token", message_id['message_id'])

def test_invalid_channel_id():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    token = bob_info['token']
    rahul = functions.auth_functions.auth_register("rahul@gmail.com", "password", "Bob", "Test")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)
    message_id = functions.message.message_send(token, channel_id['channel_id'], "hello")
    with pytest.raises(functions.errors.AccessError):
        functions.message.message_pin(rahul['token'], message_id['message_id'])

def test_invalid_message_id():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    functions.channel.channels_create(bob_info['token'], "Pycharmers", True)
    with pytest.raises(ValueError):
        functions.message.message_pin(bob_info['token'], 10001230005)
