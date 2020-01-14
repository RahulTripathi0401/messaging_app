''' Pytests written to test the 'message_edit' function '''
# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument
import pytest
import functions.general
import functions.errors
import functions.message
import functions.auth_functions
import functions.channel
import functions.helper_tokens

@pytest.fixture
def remove_fixture():
    functions.general.clearDatabase()
    token = functions.auth_functions.auth_register("email@email.com", "password", "email", "man")
    return token

def test_messages_does_not_exists(remove_fixture):
    token = functions.auth_functions.auth_login("email@email.com", "password")
    with pytest.raises(ValueError):
        functions.message.message_remove(token['token'], -1)

def test_messages_does_not_exists2(remove_fixture):
    token = functions.auth_functions.auth_login("email@email.com", "password")
    channel = functions.channel.channels_create(token['token'], "Pycharmers", True)
    message = functions.message.message_send(token['token'], channel['channel_id'], "Hello")
    with pytest.raises(ValueError):
        functions.message.message_remove(token['token'], message['message_id'] + 5)

def test_message_not_sent_by_user(remove_fixture):
    channel = functions.channel.channels_create(remove_fixture['token'], "Pycharmers", True)
    tok = remove_fixture['token']
    message = functions.message.message_send(tok, channel['channel_id'], "Hello")
    token = functions.auth_functions.auth_register("newguy@email.com", "password", "new", "guy")
    functions.channel.channel_join(token['token'], channel['channel_id'])
    with pytest.raises(functions.errors.AccessError):
        functions.message.message_remove(token['token'], message['message_id'])

# should successfully remove someone elses message if owner
def test_message_not_sent_by_owner(remove_fixture):
    token = functions.auth_functions.auth_login("email@email.com", "password")
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    channelid = functions.channel.channels_create(token['token'], "Pycharmers", True)
    functions.channel.channel_join(bob_info['token'], channelid['channel_id'])
    mid = functions.message.message_send(bob_info['token'], channelid['channel_id'], "Test")
    tok = bob_info['token']
    curr_id = channelid['channel_id']
    assert functions.channel.channel_messages(tok, curr_id, 0)['messages'][0]['message'] == "Test"
    functions.message.message_remove(token['token'], mid["message_id"])
    assert len(functions.channel.channel_messages(tok, curr_id, 0)['messages']) == 0

#removing message in channel user isnt in
def test_message_not_sent_by_admin(remove_fixture):
    token = functions.auth_functions.auth_login("email@email.com", "password")
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    channelid = functions.channel.channels_create(token['token'], "Pycharmers", True)
    functions.channel.channel_join(bob_info['token'], channelid['channel_id'])
    mid = functions.message.message_send(bob_info['token'], channelid['channel_id'], "Test message")
    functions.channel.channel_leave(bob_info['token'], channelid['channel_id'])
    with pytest.raises(functions.errors.AccessError):
        functions.message.message_remove(bob_info['token'], mid['message_id'])

def test_simple_remove(remove_fixture):
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    token = bob_info['token']
    channelid = functions.channel.channels_create(token, "Pycharmers", True)['channel_id']
    mid = functions.message.message_send(bob_info['token'], channelid, "this is a message")
    message = functions.channel.channel_messages(bob_info['token'], channelid, 0)
    assert message['messages'][0]['message'] == 'this is a message'
    functions.message.message_remove(bob_info['token'], mid['message_id'])
    message = functions.channel.channel_messages(bob_info['token'], channelid, 0)
    assert message['messages'] == []

# wrong token type
def test_wrong_token_type(remove_fixture):
    with pytest.raises(TypeError):
        functions.message.message_remove(123, 10001230001)

# wrong message_id type
def test_wrong_message_id_type(remove_fixture):
    with pytest.raises(TypeError):
        functions.message.message_remove(remove_fixture['token'], "m_id")

# invalid token
def test_invalid_token(remove_fixture):
    with pytest.raises(functions.errors.AccessError):
        functions.message.message_remove("token", 10001230001)
