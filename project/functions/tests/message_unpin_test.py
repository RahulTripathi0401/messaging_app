'''
Given a message within a channel, remove it's mark as unpinned
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
    messageid = functions.message.message_send(bob_info['token'], channel_id['channel_id'], "hello")
    functions.message.message_pin(bob_info['token'], messageid['message_id'])
    with pytest.raises(ValueError):
        functions.message.message_unpin(bob_info["token"], 10001230005)

def test_general():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)
    messageid = functions.message.message_send(bob_info['token'], channel_id['channel_id'], "hello")
    functions.message.message_pin(bob_info['token'], messageid['message_id'])
    functions.message.message_unpin(bob_info['token'], messageid['message_id'])
    messages = functions.channel.channel_messages(bob_info['token'], channel_id['channel_id'], 0)
    assert not messages['messages'][0]['is_pinned']

def test_already_unpinned():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)
    messageid = functions.message.message_send(bob_info['token'], channel_id['channel_id'], "hello")
    functions.message.message_pin(bob_info['token'], messageid['message_id'])
    functions.message.message_unpin(bob_info['token'], messageid['message_id'])
    messages = functions.channel.channel_messages(bob_info['token'], channel_id['channel_id'], 0)
    assert not messages['messages'][0]['is_pinned']
    with pytest.raises(ValueError):
        functions.message.message_unpin(bob_info['token'], messageid['message_id'])

def test_no_admin():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    rahul = functions.auth_functions.auth_register("rahul@gmail.com", "password", "rahul", "Test")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)
    functions.channel.channel_join(rahul['token'], channel_id['channel_id'])
    messageid = functions.message.message_send(bob_info['token'], channel_id['channel_id'], "hello")
    with pytest.raises(ValueError):
        functions.message.message_unpin(rahul['token'], messageid['message_id'])

def test_no_user():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)
    messageid = functions.message.message_send(bob_info['token'], channel_id['channel_id'], "hello")
    functions.message.message_pin(bob_info['token'], messageid['message_id'])
    functions.channel.channel_leave(bob_info['token'], channel_id['channel_id'])
    with pytest.raises(functions.errors.AccessError):
        functions.message.message_unpin(bob_info['token'], messageid['message_id'])

def test_token_string():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)
    messageid = functions.message.message_send(bob_info['token'], channel_id['channel_id'], "hello")
    with pytest.raises(TypeError):
        functions.message.message_unpin(123, messageid['message_id'])

def test_message_int():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    with pytest.raises(TypeError):
        functions.message.message_unpin(bob_info['token'], "hello")

def test_invalid_uid():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)
    messageid = functions.message.message_send(bob_info['token'], channel_id['channel_id'], "hello")
    with pytest.raises(functions.errors.AccessError):
        functions.message.message_pin("token", messageid['message_id'])

def test_invalid_user():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    rahul = functions.auth_functions.auth_register("rahul@gmail.com", "password", "Bob", "Test")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)
    messageid = functions.message.message_send(bob_info['token'], channel_id['channel_id'], "hello")
    functions.message.message_pin(bob_info['token'], messageid['message_id'])
    with pytest.raises(functions.errors.AccessError):
        functions.message.message_pin(rahul['token'], messageid['message_id'])

def test_invalid_token():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)
    messageid = functions.message.message_send(bob_info['token'], channel_id['channel_id'], "hello")
    functions.message.message_pin(bob_info['token'], messageid['message_id'])
    with pytest.raises(functions.errors.AccessError):
        functions.message.message_unpin("token", messageid['message_id'])

def test_not_in_channel():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    rahul = functions.auth_functions.auth_register("rahul@gmail.com", "password", "Bob", "Test")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)
    messageid = functions.message.message_send(bob_info['token'], channel_id['channel_id'], "hello")
    functions.message.message_pin(bob_info['token'], messageid['message_id'])
    with pytest.raises(functions.errors.AccessError):
        functions.message.message_unpin(rahul['token'], messageid['message_id'])
