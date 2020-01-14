''' Pytests written to test the 'functions.channel.channel_leave' function '''
import pytest
# from functions.channel.channel_leave import functions.channel.channel_leave
# from functions.channel.channel_details import functions.channel.channel_details
# from functions.channel.channel_join import functions.channel.channel_join
# from functions.channel.channel_invite import functions.channel.channel_invite
# from functions.channel.channel_messages import functions.channel.channel_messages
# from functions.channel.channels_create import functions.channel.channels_create
# from functions.auth_functions.auth_register import functions.auth_functions.auth_register
# from general import functions.general.clearDatabase
# from functions.errors import functions.errors.AccessError
import functions.channel
import functions.auth_functions
import functions.general
import functions.errors


def test_simple():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)['channel_id']
    assert functions.channel.channel_leave(bob_info['token'], channel_id) == {}


def test_invalid_channel_id():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    with pytest.raises(ValueError):
        functions.channel.channel_leave(bob_info['token'], -1)


def test_invalid_token():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)['channel_id']
    with pytest.raises(functions.errors.AccessError):
        functions.channel.channel_leave("badToken", channel_id)


def test_wrong_token_type():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)['channel_id']
    with pytest.raises(TypeError):
        functions.channel.channel_leave(12345, channel_id)


def test_wrong_channel_id_type():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    with pytest.raises(TypeError):
        functions.channel.channel_leave(bob_info['token'], "channel_id")

# invited person leaving


def test_invited_leaves():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    tom_info = functions.auth_functions.auth_register("tom@gmail.com", "password", "Tom", "Best")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)['channel_id']
    functions.channel.channel_invite(bob_info['token'], channel_id, tom_info['u_id'])
    file = open("port.txt", "r")
    portNum = str(int(file.read()))
    bob_object = {"u_id": bob_info['u_id'], "name_first": "Bob",
                  "name_last": "Test", 'profile_img_url': 'http://localhost:' + portNum + '/static/default.png'}
    tom_object = {"u_id": tom_info['u_id'], "name_first": "Tom",
                  "name_last": "Best", 'profile_img_url': 'http://localhost:' + portNum + '/static/default.png'}
    members_list = [bob_object, tom_object]
    assert functions.channel.channel_details(bob_info['token'], channel_id) == {
        "name": 'Pycharmers', "owner_members": members_list, "all_members": members_list}
    functions.channel.channel_leave(tom_info['token'], channel_id)
    members_list = [bob_object]
    assert functions.channel.channel_details(bob_info['token'], channel_id) == {
        "name": 'Pycharmers', "owner_members": members_list, "all_members": members_list}
    with pytest.raises(functions.errors.AccessError):
        functions.channel.channel_messages(tom_info['token'], channel_id, 0)

# joined person leaving


def test_joined_leaves():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    tom_info = functions.auth_functions.auth_register("tom@gmail.com", "password", "Tom", "Best")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)['channel_id']
    functions.channel.channel_join(tom_info['token'], channel_id)
    file = open("port.txt", "r")
    portNum = str(int(file.read()))
    bob_object = {"u_id": bob_info['u_id'], "name_first": "Bob",
                  "name_last": "Test", 'profile_img_url': 'http://localhost:' + portNum + '/static/default.png'}
    tom_object = {"u_id": tom_info['u_id'], "name_first": "Tom",
                  "name_last": "Best", 'profile_img_url': 'http://localhost:' + portNum + '/static/default.png'}
    members_list = [bob_object, tom_object]
    owners_list = [bob_object]
    assert functions.channel.channel_details(bob_info['token'], channel_id) == {
        "name": 'Pycharmers', "owner_members": owners_list, "all_members": members_list}
    functions.channel.channel_leave(tom_info['token'], channel_id)
    assert functions.channel.channel_details(bob_info['token'], channel_id) == {
        "name": 'Pycharmers', "owner_members": owners_list, "all_members": owners_list}
    with pytest.raises(functions.errors.AccessError):
        functions.channel.channel_messages(tom_info['token'], channel_id, 0)

# person who never joined trying to leave


def test_outsider_leaves():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    tom_info = functions.auth_functions.auth_register("tom@gmail.com", "password", "Tom", "Best")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)['channel_id']
    file = open("port.txt", "r")
    portNum = str(int(file.read()))
    bob_object = {"u_id": bob_info['u_id'], "name_first": "Bob",
                  "name_last": "Test", 'profile_img_url': 'http://localhost:' + portNum + '/static/default.png'}
    members_list = [bob_object]
    assert functions.channel.channel_details(bob_info['token'], channel_id) == {
        "name": 'Pycharmers', "owner_members": members_list, "all_members": members_list}
    with pytest.raises(functions.errors.AccessError):
        functions.channel.channel_leave(tom_info['token'], channel_id)
