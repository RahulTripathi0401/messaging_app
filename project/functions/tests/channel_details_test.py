'''
Find and key information about a channel
'''
import pytest
import functions.channel
import functions.auth_functions
import functions.errors
import functions.general

def test_simple():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)['channel_id']
    file = open("port.txt", "r")
    portNum = str(int(file.read()))
    members_list = [{"u_id": bob_info['u_id'], "name_first": "Bob", "name_last": "Test", 'profile_img_url': 'http://localhost:' + portNum + '/static/default.png'}]
    utest = {"name": 'Pycharmers', "owner_members": members_list, "all_members": members_list}
    assert functions.channel.channel_details(bob_info['token'], channel_id) == utest

def test_invalid_channel_id():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    with pytest.raises(ValueError):
        functions.channel.channel_details(bob_info['token'], -1)

def test_unauthorised_user():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)['channel_id']
    with pytest.raises(functions.errors.AccessError):
        functions.channel.channel_details("badToken", channel_id)

def test_user_not_in_channel():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    james_info = functions.auth_functions.auth_register("james@gmail.com", "password", "james", "Test")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)['channel_id']
    with pytest.raises(functions.errors.AccessError):
        functions.channel.channel_details(james_info['token'], channel_id)

def test_wrong_token_type():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)['channel_id']
    with pytest.raises(TypeError):
        functions.channel.channel_details(12345, channel_id)

def test_wrong_channel_id_type():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    with pytest.raises(TypeError):
        functions.channel.channel_details(bob_info['token'], "channel_id")
