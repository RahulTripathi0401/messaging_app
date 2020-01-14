'''
Given a message within a channel the authorised user is part of, remove a
"react" to that particular message
'''
import pytest
import functions.general
import functions.errors
import functions.message
import functions.auth_functions
import functions.channel
import functions.helper_tokens

def test_general():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)
    messages = functions.message.message_send(bob_info['token'], channel_id['channel_id'], "hello")
    functions.message.message_react(bob_info['token'], messages['message_id'], 1)
    functions.message.message_unreact(bob_info['token'], messages['message_id'], 1)
    messages = functions.channel.channel_messages(bob_info['token'], channel_id['channel_id'], 0)
    assert not messages['messages'][0]['reacts'][0]['is_this_user_reacted']

def test_invalid_react_id():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)
    messages = functions.message.message_send(bob_info['token'], channel_id['channel_id'], "hello")
    functions.message.message_react(bob_info['token'], messages['message_id'], 1)
    with pytest.raises(ValueError):
        functions.message.message_unreact(bob_info['token'], messages['message_id'], -1)

def test_invalid_tokenr():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)
    messages = functions.message.message_send(bob_info['token'], channel_id['channel_id'], "hello")
    functions.message.message_react(bob_info['token'], messages['message_id'], 1)
    with pytest.raises(functions.errors.AccessError):
        functions.message.message_unreact("token", messages['message_id'], 1)

def test_already_unreacted():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)
    messages = functions.message.message_send(bob_info['token'], channel_id['channel_id'], "hello")
    functions.message.message_react(bob_info['token'], messages['message_id'], 1)
    functions.message.message_unreact(bob_info['token'], messages['message_id'], 1)
    with pytest.raises(ValueError):
        functions.message.message_unreact(bob_info['token'], messages['message_id'], 1)

def test_no_message_sent():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)
    messages = functions.message.message_send(bob_info['token'], channel_id['channel_id'], "hello")
    with pytest.raises(ValueError):
        functions.message.message_unreact(bob_info['token'], messages['message_id'], 1)

def test_token_not_str():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)
    messages = functions.message.message_send(bob_info['token'], channel_id['channel_id'], "hello")
    functions.message.message_react(bob_info['token'], messages['message_id'], 1)
    with pytest.raises(TypeError):
        functions.message.message_unreact(123, messages['message_id'], 1)

def test_react_not_int():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)
    messages = functions.message.message_send(bob_info['token'], channel_id['channel_id'], "hello")
    functions.message.message_react(bob_info['token'], messages['message_id'], 1)
    with pytest.raises(TypeError):
        functions.message.message_unreact(bob_info['token'], messages['message_id'], "hello")

def test_messageid_not_int():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)
    messages = functions.message.message_send(bob_info['token'], channel_id['channel_id'], "hello")
    functions.message.message_react(bob_info['token'], messages['message_id'], 1)
    with pytest.raises(TypeError):
        functions.message.message_unreact(bob_info['token'], "hello", 1)

def test_invalid_channel():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)
    messages = functions.message.message_send(bob_info['token'], channel_id['channel_id'], "hello")
    functions.message.message_react(bob_info['token'], messages['message_id'], 1)
    with pytest.raises(ValueError):
        functions.message.message_unreact(bob_info['token'], 20001230001, 1)

def test_wrong_user():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    rahul = functions.auth_functions.auth_register("rahul@gmail.com", "password", "rahul", "Test")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)
    messages = functions.message.message_send(bob_info['token'], channel_id['channel_id'], "hello")
    functions.message.message_react(bob_info['token'], messages['message_id'], 1)
    with pytest.raises(functions.errors.AccessError):
        functions.message.message_unreact(rahul['token'], messages['message_id'], 1)
