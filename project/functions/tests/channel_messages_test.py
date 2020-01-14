''' Pytests written to test the 'functions.channel.channel_messages' function '''
import pytest
import functions.channel
import functions.auth_functions
import functions.general
import functions.errors

@pytest.fixture
def user_info():
    functions.general.clearDatabase()
    slackr_owner = functions.auth_functions.auth_register("la@gmail.com", "validpass", "fname", "lname")
    channel_owner = functions.auth_functions.auth_register("bennyjones@gmail.com", "passyword", "Ben", "Jones")
    member = functions.auth_functions.auth_register("sarahc@yahoo.com.au", "whatsup", "Sarah", "Callahan")
    non_member = functions.auth_functions.auth_register("john@gmail.com", "Yellowrocks", "John", "Smith")
    # makes a private channel for channel_owner
    channel_reply = functions.channel.channels_create(channel_owner['token'], "Bens_channel", True)
    channel_owner['own_channel_ids'] = channel_reply['channel_id']
    functions.message.message_send(channel_owner['token'], channel_owner['own_channel_ids'], "Testing one two three")
    message_dict = functions.channel.channel_messages(channel_owner['token'], channel_owner['own_channel_ids'], 0)
    functions.channel.channel_join(member['token'], channel_owner['own_channel_ids'])
    channel_owner['messages'] = message_dict['messages']
    return slackr_owner, channel_owner, member, non_member


def test_simple():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)['channel_id']
    functions.message.message_send(bob_info['token'], channel_id, "test message")
    functions.channel.channel_messages_return = functions.channel.channel_messages(bob_info['token'], channel_id, 0)
    assert functions.channel.channel_messages_return['start'] == 0
    assert functions.channel.channel_messages_return['end'] == -1
    assert functions.channel.channel_messages_return['messages'][0]['message'] == "test message"
    assert functions.channel.channel_messages_return['messages'][0]['u_id'] == functions.helper_tokens.token_u_id(bob_info['token'])


def test_invalid_channel_id():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    with pytest.raises(ValueError):
        functions.channel.channel_messages(bob_info['token'], -1, 0)


# only channel members, Slackr owners and admins can view a channel's messages
def test_nonmember_permission(user_info):
    non_member = user_info[3]
    channel_owner = user_info[1]
    with pytest.raises(functions.errors.AccessError, match="Not a channel member"):
        functions.channel.channel_messages(non_member['token'], channel_owner['own_channel_ids'], 0)


def test_invalid_start():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)['channel_id']
    with pytest.raises(ValueError):
        functions.channel.channel_messages(bob_info['token'], channel_id, 205)


def test_unauthorised_user():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)['channel_id']
    with pytest.raises(functions.errors.AccessError):
        functions.channel.channel_messages("badToken", channel_id, 0)


def test_wrong_token_type():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)['channel_id']
    with pytest.raises(TypeError):
        functions.channel.channel_messages(12345, channel_id, 0)


def test_wrong_channel_id_type():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    with pytest.raises(TypeError):
        functions.channel.channel_messages(bob_info['token'], "channel_id", 0)


def test_wrong_start_type():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)['channel_id']
    with pytest.raises(TypeError):
        functions.channel.channel_messages(bob_info['token'], channel_id, "start")


# oldest messages displayed last
# -1 is used to indicate end of messages on this page
# no more than 50 messages are displayed at a time
def test_pagination():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)['channel_id']
    for i in range(124):
        functions.message.message_send(bob_info['token'], channel_id, f"test message {123 - i}")
    for start in range(124):
        functions.channel.channel_messages_return = functions.channel.channel_messages(bob_info['token'], channel_id, start)
        assert len(functions.channel.channel_messages_return['messages']) <= 50
        assert functions.channel.channel_messages_return['start'] == start
        if start + 50 <= 124:
            assert functions.channel.channel_messages_return['end'] == start + 50
        else:
            assert functions.channel.channel_messages_return['end'] == -1
        for i in range(len(functions.channel.channel_messages_return['messages'])):
            assert functions.channel.channel_messages_return['messages'][i]['message'] == f"test message {start + i}"
            assert functions.channel.channel_messages_return['messages'][i]['u_id'] == bob_info['u_id']
            assert functions.channel.channel_messages_return['messages'][i]['message_id'] == \
                    int(str(channel_id) + "000123000" + str(124-(start+i)))


def test_empty_messages():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)['channel_id']
    functions.channel.channel_messages_return = functions.channel.channel_messages(bob_info['token'], channel_id, 0)
    assert functions.channel.channel_messages_return['messages'] == []
    assert functions.channel.channel_messages_return['start'] == 0
    assert functions.channel.channel_messages_return['end'] == -1
