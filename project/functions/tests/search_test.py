''' Pytests written to test the 'functions.channel.search' function '''
import pytest
import functions.general
import functions.errors
import functions.channel
import functions.auth_functions
import functions.message


@pytest.fixture
def permission_info():
    functions.general.clearDatabase()
    slackr_owner = functions.auth_functions.auth_register("la@gmail.com", "validpass", "fname", "lname")
    channel_owner = functions.auth_functions.auth_register("bennyjones@gmail.com", "passyword", "Ben", "Jones")
    member = functions.auth_functions.auth_register("sarahc@yahoo.com.au", "whatsup", "Sarah", "Callahan")
    non_member = functions.auth_functions.auth_register("john@gmail.com", "Yellowrocks", "John", "Smith")
    #makes a private channel for channel_owner
    channel_reply = functions.channel.channels_create(channel_owner['token'], "Bens_channel", False)
    channel_owner['own_channel_ids'] = channel_reply['channel_id']
    functions.message.message_send(channel_owner['token'], channel_owner['own_channel_ids'], "Testing one two three")
    message_dict = functions.channel.channel_messages(channel_owner['token'], channel_owner['own_channel_ids'], 0)
    functions.channel.channel_invite(channel_owner['token'], channel_owner['own_channel_ids'], member['u_id'])
    channel_owner['messages'] = message_dict['messages']
    return slackr_owner, channel_owner, member, non_member

def test_success(permission_info):
    channel_owner = permission_info[1]
    assert functions.channel.search(channel_owner['token'], "Testing") == {'messages':channel_owner['messages']}

def test_invalid_token():
    with pytest.raises(TypeError, match=r"Token should be string"):
        functions.channel.search(12, "Hello")

def test_invalid_query(permission_info):
    channel_owner = permission_info[1]
    with pytest.raises(TypeError, match=r"Query should be string"):
        functions.channel.search(channel_owner['token'], 12)

def test_member(permission_info):
    member = permission_info[2]
    channel_owner = permission_info[1]
    assert functions.channel.search(member['token'], "Testing") == {'messages':channel_owner['messages']}

#Non-members cannot view messages within a channel
def test_non_member(permission_info):
    non_member = permission_info[3]
    assert functions.channel.search(non_member['token'], "Testing") == {'messages':[]}

#Admins and owners of the Slackr can also functions.channel.search within all channels
def test_slackr_owner(permission_info):
    slackr_owner = permission_info[0]
    channel_owner = permission_info[1]
    assert functions.channel.search(slackr_owner['token'], "Testing") == {'messages':channel_owner['messages']}

#Value error for incorrect token
def test_invalid_token_str(permission_info):
    with pytest.raises(functions.errors.AccessError, match=r".*"):
        functions.channel.search("bad_token", "Blah")

#Value error for functions.channel.search longer than 100 characters
def test_long_search(permission_info):
    user = permission_info[1]
    with pytest.raises(ValueError, match=r".*"):
        functions.channel.search(user['token'], "wd3U8whlmQlBjJ7TVVGbPzQCHq8uKMqqgAx80KjbWa5APr2Lq" + \
               "GsOGCLOAPJXocWPFCzZxXkBmRuZWB5ZVotQsE5WjMAIDsKbibaJI")

#Type error, query not a string
def test_not_string(permission_info):
    user = permission_info[1]
    with pytest.raises(TypeError, match=r".*"):
        functions.channel.search(user['token'], 234)
