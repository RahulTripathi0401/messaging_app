''' Pytests written to test the 'functions.message.message_send' function '''
import pytest
import functions.general
import functions.errors
import functions.message
import functions.auth_functions
import functions.channel
import functions.helper_tokens

@pytest.fixture
def user_info():
    functions.general.clearDatabase()
    slackr_owner = functions.auth_functions.auth_register("la@gmail.com", "validpass", "f", "le")
    channel_owner = functions.auth_functions.auth_register("b@gmail.com", "passywod", "B", "J")
    member = functions.auth_functions.auth_register("s@yahoo.com.au", "whatsup", "S", "C")
    non_member = functions.auth_functions.auth_register("j@gmail.com", "Yellowrocks", "J", "S")
    # makes a private channel for channel_owner
    channel_reply = functions.channel.channels_create(channel_owner['token'], "Bens_channel", False)
    channel_owner['own_channel_ids'] = channel_reply['channel_id']
    token = channel_owner['token']
    functions.message.message_send(token, channel_owner['own_channel_ids'], "Testing one two three")
    message_dict = functions.channel.channel_messages(token, channel_owner['own_channel_ids'], 0)
    functions.channel.channel_invite(token, channel_owner['own_channel_ids'], member['u_id'])
    channel_owner['messages'] = message_dict['messages']
    return slackr_owner, channel_owner, member, non_member

# The user can send and edit messages within a stream in a channel
def test_message_send(user_info):
    member = user_info[2]
    owner = user_info[1]
    token = member['token']
    assert functions.message.message_send(token, owner['own_channel_ids'], 'Welcome') == {
        'message_id': 10001230002}
    message_request = functions.channel.channel_messages(token, owner['own_channel_ids'], 0)
    assert len(message_request['messages']) == 2
    assert message_request['messages'][0]['message'] == "Welcome"
    assert message_request['messages'][1]['message'] == "Testing one two three"

def test_invalid_token(user_info):
    owner = user_info[1]
    with pytest.raises(TypeError, match=".*"):
        functions.message.message_send(12345, owner['own_channel_ids'], "Hello")

def test_invalid_channel_id(user_info):
    owner = user_info[1]
    with pytest.raises(TypeError, match=".*"):
        functions.message.message_send(owner['token'], "bobo", "Hello")

def test_invalid_message(user_info):
    owner = user_info[1]
    with pytest.raises(TypeError, match=".*"):
        functions.message.message_send(owner['token'], owner['own_channel_ids'], 12)

def test_nonexistent_channel(user_info):
    owner = user_info[1]
    with pytest.raises(ValueError, match=".*"):
        functions.message.message_send(owner['token'], 3000, "Hello")

def test_nonexistent_user(user_info):
    owner = user_info[1]
    with pytest.raises(functions.errors.AccessError, match=".*"):
        functions.message.message_send("lfkdnkn", owner['own_channel_ids'], "Hello")

# Each message cannot be longer than 1000 characters
def test_message_length(user_info):
    member = user_info[2]
    owner = user_info[1]
    message = "a" * 1001
    with pytest.raises(ValueError):
        functions.message.message_send(member['token'], owner['own_channel_ids'], message)


# Only channel members (or Slack admins and owners) can post to the channel
def test_message_permissions(user_info):
    non_member = user_info[3]
    owner = user_info[1]
    token = non_member['token']
    with pytest.raises(functions.errors.AccessError):
        functions.message.message_send(token, owner['own_channel_ids'], "Not a member")


# Slackr owners can send messages in all channels
def test_slackr_owner_permissions(user_info):
    slackr_owner = user_info[0]
    channel_owner = user_info[1]
    token = slackr_owner['token']
    owner = channel_owner['own_channel_ids']
    assert functions.message.message_send(token, owner, "I") == {'message_id': 10001230002}
    message_request = functions.channel.channel_messages(token, owner, 0)
    assert len(message_request['messages']) == 2
    assert message_request['messages'][0]['message'] == "I"
    assert message_request['messages'][1]['message'] == "Testing one two three"


def test_user_in_channel():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    channel_id = functions.channel.channels_create(bob_info['token'], "name", True)
    members = functions.channel.channel_details(bob_info['token'], channel_id['channel_id'])
    assert members['owner_members'][0]['name_first'] == "Bob"


def test_message_send_no_message_sent():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    token = bob_info['token']
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)
    view_channel = functions.channel.channel_messages(token, channel_id['channel_id'], 0)
    assert len(view_channel['messages']) == 0


def test_message_send_simple_further():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)
    functions.message.message_send(bob_info['token'], channel_id['channel_id'], "this is a message")
    message = functions.channel.channel_messages(bob_info['token'], channel_id['channel_id'], 0)
    assert message['messages'][0]['message'] == 'this is a message'
