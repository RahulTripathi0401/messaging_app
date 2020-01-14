''' Pytests written to test the 'functions.auth_functions.admin_userpermission_change' function '''
import pytest
import functions.auth_functions
import functions.channel
import functions.general
import functions.errors


@pytest.fixture
def permission_info():
    functions.general.clearDatabase()
    owner = functions.auth_functions.auth_register("user@gmail.com", "validpass", "fname", "lname")
    # makes given token holder channel owner
    channel_reply = functions.channel.channels_create(owner['token'], "Owner channel", False)
    owner['own_channel_ids'] = channel_reply['channel_id']
    # create a second user to give ownership to
    owner2 = functions.auth_functions.auth_register("newowner@gmail.com", "pass83", "Joe", "Malone")
    owner2['own_channel_ids'] = owner['own_channel_ids']
    member = functions.auth_functions.auth_register("benny@yahoo.com.au", "password12", "benny", "jones")
    # should work since Benny Jones is a new user
    new_channel = functions.channel.channels_create(member['token'], "Member channel", False)
    member['own_channel_ids'] = new_channel['channel_id']
    # member becomes separate channel owner
    # Access Error if sole owner becomes non-owner
    # See sole_owner_leaves test
    return owner, owner2, member


def test_simple(permission_info):
    owner = permission_info[0]
    owner.pop('owner_channel_ids', None)
    # change owner to admin
    assert functions.auth_functions.admin_userpermission_change(owner['token'], owner['u_id'], 2) == {}


def test_invalid_uid(permission_info):
    owner = permission_info[1]
    with pytest.raises(TypeError, match=r".*"):
        functions.auth_functions.admin_userpermission_change(owner['token'], "h", 2)


def test_nonexistent_uid(permission_info):
    owner = permission_info[1]
    with pytest.raises(ValueError, match=r".*"):
        functions.auth_functions.admin_userpermission_change(owner['token'], 0, 2)


def test_invalid_token(permission_info):
    owner = permission_info[1]
    with pytest.raises(TypeError, match=r".*"):
        functions.auth_functions.admin_userpermission_change(1233, owner['u_id'], 2)


def test_nonexistent_user_token(permission_info):
    owner = permission_info[1]
    with pytest.raises(functions.errors.AccessError, match=r".*"):
        functions.auth_functions.admin_userpermission_change("hg", owner['u_id'], 2)


def test_invalid_permission_id_type(permission_info):
    owner = permission_info[1]
    member = permission_info[2]
    with pytest.raises(TypeError, match=r".*"):
        functions.auth_functions.admin_userpermission_change(owner['token'], member['u_id'], "blah")


# test if permission id is valid
# only 1-owner,2-admin and 3-member are valid permission ids
def test_invalid_permission_id(permission_info):
    owner = permission_info[1]
    member = permission_info[2]
    with pytest.raises(ValueError, match=r".*"):
        functions.auth_functions.admin_userpermission_change(owner['token'], member['u_id'], 1234)


def test_inappropriate_permisson_change(permission_info):
    owner = permission_info[0]
    member = permission_info[2]
    with pytest.raises(functions.errors.AccessError, match=r".*"):
        functions.auth_functions.admin_userpermission_change(member['token'], owner['u_id'], 3)


# authorised user not admin or owner
# assumes first user (auto-admin) already been created
def test_inappropriate_authorised_user(permission_info):
    member = permission_info[2]
    with pytest.raises(functions.errors.AccessError, match=r".*"):
        functions.auth_functions.admin_userpermission_change(member['token'], member['u_id'], 2)


# setting same permissions as user currently has
def test_already_permission(permission_info):
    owner = permission_info[1]
    member = permission_info[2]
    with pytest.raises(functions.errors.AccessError, match=r".*"):
        functions.auth_functions.admin_userpermission_change(owner['token'], member['u_id'], 3)


def test_sole_owner_leaves(permission_info):
    member = permission_info[2]
    with pytest.raises(functions.errors.AccessError, match=r".*"):
        functions.auth_functions.admin_userpermission_change(member['token'], member['u_id'], 3)
