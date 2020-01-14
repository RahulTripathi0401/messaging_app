''' Pytests written to test the 'functions.channel.channel_join' function '''
import pytest
import functions.channel
import functions.auth_functions
import functions.general
import functions.errors



def test_simple():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    tom_info = functions.auth_functions.auth_register("tom@gmail.com", "password", "Tom", "Best")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)['channel_id']
    file = open("port.txt", "r")
    portNum = str(int(file.read()))
    bob_object = {"u_id": bob_info['u_id'], "name_first": "Bob",
                  "name_last": "Test", 'profile_img_url': 'http://localhost:' + portNum + '/static/default.png'}
    tom_object = {"u_id": tom_info['u_id'], "name_first": "Tom",
                  "name_last": "Best", 'profile_img_url': 'http://localhost:' + portNum + '/static/default.png'}
    assert functions.channel.channel_details(bob_info['token'], channel_id)['all_members'] == [bob_object]
    assert functions.channel.channel_join(tom_info['token'], channel_id) == {}
    owner_list = [bob_object]
    member_list = [bob_object, tom_object]
    assert functions.channel.channel_details(bob_info['token'], channel_id) == {
        "name": 'Pycharmers', "owner_members": owner_list, "all_members": member_list}


def test_invalid_token():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)['channel_id']
    with pytest.raises(functions.errors.AccessError):
        functions.channel.channel_join("badToken", channel_id)


def test_invalid_channel_id():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    with pytest.raises(ValueError):
        functions.channel.channel_join(bob_info['token'], -1)


def test_wrong_token_type():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)['channel_id']
    with pytest.raises(TypeError):
        functions.channel.channel_join(12345, channel_id)


def test_wrong_channel_id_type():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    with pytest.raises(TypeError):
        functions.channel.channel_join(bob_info['token'], "channel_id")


# trying to join a channel you're already a part of
def test_join_twice():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)['channel_id']
    with pytest.raises(functions.errors.AccessError):
        functions.channel.channel_join(bob_info['token'], channel_id)


# trying to join a private channel
def test_join_private():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    tom_info = functions.auth_functions.auth_register("tom@gmail.com", "password", "Tom", "Best")
    channel_id = functions.channel.channels_create(tom_info['token'], "Pycharmers", False)['channel_id']
    with pytest.raises(functions.errors.AccessError):
        functions.channel.channel_join(bob_info['token'], channel_id)


# owner joining a private channel
def test_admin_private():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    tom_info = functions.auth_functions.auth_register("tom@gmail.com", "password", "Tom", "Best")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", False)['channel_id']
    with pytest.raises(functions.errors.AccessError):
        functions.channel.channel_join(tom_info['token'], channel_id)
