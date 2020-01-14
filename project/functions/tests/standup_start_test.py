''' Pytests written to test the 'functions.standup.standup_start' function '''
from datetime import datetime, timedelta
import pytest
import functions.standup
import functions.auth_functions
import functions.channel
import functions.general
import functions.errors
import server

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
    channel_reply = functions.channel.channels_create(channel_owner['token'], "Bens_channel", True)
    channel_owner['own_channel_ids'] = channel_reply['channel_id']
    admin['admin_channel_ids'] = channel_owner['own_channel_ids']
    functions.channel.channel_join(member['token'], channel_owner['own_channel_ids'])
    member['member_channel_ids'] = channel_owner['own_channel_ids']
    return slackr_owner, channel_owner, admin, member, non_member


# test function outputs timestamp string
def test_datetime_format(permission_info):
    owner = permission_info[1]
    finish_time = functions.standup.standup_start(owner['token'], owner['own_channel_ids'], 900)
    finished = float(finish_time['time_finish'])
    finished_object = datetime.fromtimestamp(finished)
    assert finished_object == datetime.fromtimestamp(finished)


# tests channel owner-generated start_standup function outputs a finish time 15 min in future
def test_is_current_time(permission_info):
    owner = permission_info[1]
    # derive object from functions.standup.standup_start fn output
    standup_dict = functions.standup.standup_start(owner['token'], owner['own_channel_ids'], 900)
    fn_finish = datetime.fromtimestamp(standup_dict['time_finish'])
    # calculate finish time in 15 minutes from now
    finish_now = functions.general.get_time()+timedelta(minutes=16)
    recent_fin = functions.general.get_time()+timedelta(minutes=13)
    assert fn_finish <= finish_now
    # test that function time returned was within 2 mins of current time + 15
    assert fn_finish >= recent_fin
    time_diff = (finish_now-fn_finish).total_seconds() / 60
    assert time_diff <= 1


# tests channel admin-generated start_standup function outputs a finish time 15 min in future
def test_is_current_time_admin(permission_info):
    admin = permission_info[2]
    owner = permission_info[1]
    # derive object from functions.standup.standup_start fn output
    standup_dict = functions.standup.standup_start(admin['token'], owner['own_channel_ids'], 900)
    fn_finish = datetime.fromtimestamp(standup_dict['time_finish'])
    # calculate finish time in 15 minutes from now
    finish_now = functions.general.get_time()+timedelta(minutes=16)
    assert fn_finish <= finish_now
    time_diff = (finish_now-fn_finish).total_seconds() / 60
    assert time_diff <= 1


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


# Access error if owner tries to start stand up when already running
def test_already_started1(owner_start):
    owner = owner_start
    with pytest.raises(ValueError, match=r".*"):
        functions.standup.standup_start(owner['token'], owner['own_channel_ids'], 900)


# if admin tries to start stand up when running
def test_already_started2(admin_start):
    admin = admin_start
    for key in server.channels:
        if server.channels[key].channel_id == admin['admin_channel_ids']:
            found_channel = server.channels[key]
            break
    assert found_channel.standup_timer is not None
    with pytest.raises(ValueError, match=r".*"):
        functions.standup.standup_start(admin['token'], admin['admin_channel_ids'], 900)


# if member tries to start stand up when running
def test_already_started3(member_start):
    member = member_start
    with pytest.raises(ValueError, match=r".*"):
        functions.standup.standup_start(member['token'], member['member_channel_ids'], 900)


# Access error if non-member tries to start stand up
def test_nonmember_start(permission_info):
    owner = permission_info[1]
    nonmember = permission_info[4]
    with pytest.raises(functions.errors.AccessError, match=r".*"):
        functions.standup.standup_start(nonmember['token'], owner['own_channel_ids'], 900)


# value error for invalid token
def test_invalid_token(permission_info):
    owner = permission_info[1]
    with pytest.raises(TypeError, match=r".*"):
        functions.standup.standup_start(12, owner['own_channel_ids'], 900)


# Value error if channel (based on ID) does not exist for owner
def test_unknown_channel_id_1(permission_info):
    owner = permission_info[1]
    with pytest.raises(ValueError, match=r".*"):
        functions.standup.standup_start(owner['token'], 2222, 900)


# for admin
def test_unknown_channel_id_2(permission_info):
    admin = permission_info[2]
    with pytest.raises(ValueError, match=r".*"):
        functions.standup.standup_start(admin['token'], 2222, 900)


# for member
def test_unknown_channel_id_3(permission_info):
    member = permission_info[3]
    with pytest.raises(ValueError, match=r".*"):
        functions.standup.standup_start(member['token'], 2222, 900)

# for non-member
def test_unknown_channel_id_4(permission_info):
    nonmember = permission_info[4]
    with pytest.raises(ValueError, match=r".*"):
        functions.standup.standup_start(nonmember['token'], 2222, 900)

def test_short_standup(permission_info):
    member = permission_info[3]
    owner = permission_info[1]
    functions.standup.standup_start(member['token'], member['member_channel_ids'], 60)['time_finish'] \
    == functions.general.get_time()+timedelta(minutes=1)

def test_long_standup(permission_info):
    member = permission_info[3]
    owner = permission_info[1]
    functions.standup.standup_start(member['token'], member['member_channel_ids'], 360000)['time_finish'] \
    == functions.general.get_time()+timedelta(minutes=60)
