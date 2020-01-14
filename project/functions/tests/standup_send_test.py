''' Pytests written to test the 'functions.standup.standup_send' function '''
import datetime
import pytest
import functions.auth_functions
import functions.channel
import functions.standup
import functions.general
import functions.errors


@pytest.fixture
def permission_info():
    functions.general.clearDatabase()
    functions.general.set_time(functions.general.get_time())
    slackr_owner = functions.auth_functions.auth_register("la@gmail.com", "validpass", "fname", "lname")
    channel_owner = functions.auth_functions.auth_register("bennyjones@gmail.com", "passyword", "Ben", "Jones")
    admin = functions.auth_functions.auth_register("admin@yahoo.com.au", "adminarthur", "Arthur", "Admin")
    functions.auth_functions.admin_userpermission_change(slackr_owner['token'], admin['u_id'], 2)
    member = functions.auth_functions.auth_register("sarahc@yahoo.com.au", "whatsup", "Sarah", "Callahan")
    non_member = functions.auth_functions.auth_register("john@gmail.com", "Yellowrocks", "John", "Smith")
    channel_reply = functions.channel.channels_create(
        channel_owner['token'], "Bens_channel", True)
    channel_owner['own_channel_ids'] = channel_reply['channel_id']
    admin['admin_channel_ids'] = channel_owner['own_channel_ids']
    functions.channel.channel_join(member['token'], channel_owner['own_channel_ids'])
    member['member_channel_ids'] = channel_owner['own_channel_ids']
    return slackr_owner, channel_owner, admin, member, non_member


# ValueError when send a standup message if no standup running
# test with owner
def test_no_standup_owner(permission_info):
    owner = permission_info[1]
    with pytest.raises(ValueError, match=r".*"):
        functions.standup.standup_send(owner['token'], owner['own_channel_ids'], "Testing")


# test with admin
def test_no_standup_admin(permission_info):
    admin = permission_info[2]
    with pytest.raises(ValueError, match=r".*"):
        functions.standup.standup_send(admin['token'], admin['admin_channel_ids'], "Testing")


# test with member
def test_no_standup_member(permission_info):
    member = permission_info[3]
    with pytest.raises(ValueError, match=r".*"):
        functions.standup.standup_send(member['token'], member['member_channel_ids'], "Testing")


# test with non-member
def test_no_standup_nonmember(permission_info):
    nonmember = permission_info[4]
    owner = permission_info[1]
    with pytest.raises(functions.errors.AccessError, match=r".*"):
        functions.standup.standup_send(nonmember['token'], owner['own_channel_ids'], "Testing")


@pytest.fixture
def owner_start(permission_info):
    owner = permission_info[1]
    owner['standup_end'] = functions.standup.standup_start(
        owner['token'], owner['own_channel_ids'], 900)
    return owner


@pytest.fixture
def admin_start(permission_info):
    admin = permission_info[2]
    admin['standup_end'] = functions.standup.standup_start(
        admin['token'], admin['admin_channel_ids'], 900)
    return admin


@pytest.fixture
def member_start(permission_info):
    member = permission_info[3]
    member['standup_end'] = functions.standup.standup_start(
        member['token'], member['member_channel_ids'], 900)
    return member


# tests that channel owner can send a standup message in own standup
def test_owner_standup_message(permission_info, owner_start):
    owner = owner_start
    admin = permission_info[2]
    member = permission_info[3]
    assert functions.standup.standup_send(owner['token'], owner['own_channel_ids'], "Hello, I'm channel owner") == {}
    # tests that admins and members can send messages in a standup started by owner
    assert functions.standup.standup_send(admin['token'], admin['admin_channel_ids'], "I'm a channel admin") == {}
    assert functions.standup.standup_send(member['token'], member['member_channel_ids'], "I'm a channel member") == {}


# tests that channel admin can send a standup message in own standup
def test_admin_standup_message(permission_info, admin_start):
    admin = admin_start
    owner = permission_info[1]
    member = permission_info[3]
    assert functions.standup.standup_send(admin['token'], admin['admin_channel_ids'],
                        "Hey, I'm a channel admin") == {}
    # tests that owners and members can send messages in a standup started by admin
    assert functions.standup.standup_send(owner['token'], owner['own_channel_ids'], "Hello, I'm channel owner") == {}
    assert functions.standup.standup_send(member['token'], member['member_channel_ids'], "I'm a channel member") == {}


# tests that channel member can send a standup message in own standup
def test_member_standup_message(permission_info, member_start):
    member = member_start
    owner = permission_info[1]
    admin = permission_info[2]
    assert functions.standup.standup_send(member['token'], member['member_channel_ids'],
                        "Hey, I'm a channel member") == {}
    # tests that owners and admins can send messages in a standup started by a member
    assert functions.standup.standup_send(owner['token'], owner['own_channel_ids'],
                        "Hello, I'm channel owner") == {}
    assert functions.standup.standup_send(admin['token'], admin['admin_channel_ids'],
                        "Hey, I'm a channel admin") == {}


#tests that a message is sent when the standup is finished
def test_standup_message(permission_info, owner_start):
    member = permission_info[3]
    messages = ['hello', 'standup', 'messages']
    standup_messages = []
    for message in messages:
        functions.standup.standup_send(member['token'], member['member_channel_ids'], message)
        standup_messages.append("sarahcallahan: " + message)
    functions.general.set_time(functions.general.get_time()+datetime.timedelta(minutes=15))
    message_dict = functions.channel.channel_messages(member['token'], member['member_channel_ids'], 0)
    assert message_dict['messages'][0]['message'] == '\n'.join(standup_messages)

# Value Error when channel id does not exist
def test_nonexistent_channel(member_start):
    member = member_start
    with pytest.raises(ValueError):
        functions.standup.standup_send(member['token'], 123, "Why is there no channel here?")


# Value Error if msg > 1000 characters
def test_long_message(member_start):
    member = member_start
    message = "a" * 1001
    with pytest.raises(ValueError):
        functions.standup.standup_send(member['token'], member['member_channel_ids'], message)


# Access Error if non-channel member sends message
def test_not_channel_member(permission_info):
    owner = permission_info[1]
    nonmember = permission_info[4]
    with pytest.raises(functions.errors.AccessError):
        functions.standup.standup_send(nonmember['token'], owner['own_channel_ids'], "Non-member message")


# Access error if user tries to send message after standup finished
def test_standup_finished(member_start):
    member = member_start
    functions.general.set_time(functions.general.get_time()+datetime.timedelta(minutes=16))
    with pytest.raises(ValueError):
        functions.standup.standup_send(member['token'], member['member_channel_ids'], 'Is it finished?')
