''' Pytests written to test the 'channel_invire' function '''
import pytest
import functions.channel
import functions.auth_functions
import functions.general
import functions.errors
import server

def test_simple():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    tom_info = functions.auth_functions.auth_register("tom@gmail.com", "password", "Tom", "Best")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)['channel_id']
    assert functions.channel.channel_invite(bob_info['token'], channel_id, tom_info['u_id']) == {}
    channel_info = functions.channel.channel_details(bob_info['token'], channel_id)
    file = open("port.txt", "r")
    portNum = str(int(file.read()))
    bob_object = {"u_id": bob_info['u_id'], "name_first": "Bob",
                  "name_last": "Test", 'profile_img_url': 'http://localhost:' + portNum + '/static/default.png'}
    tom_object = {"u_id": tom_info['u_id'], "name_first": "Tom",
                  "name_last": "Best", 'profile_img_url': 'http://localhost:' + portNum + '/static/default.png'}

    assert bob_object in channel_info['owner_members']
    assert bob_object in channel_info['all_members']
    assert tom_object in channel_info['owner_members']
    assert tom_object in channel_info['all_members']

def test_invalid_channel_id():
    functions.general.clearDatabase()
    token = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")['token']
    u_id = functions.auth_functions.auth_register("tom@gmail.com", "password", "Tom", "Best")['u_id']
    with pytest.raises(ValueError):
        functions.channel.channel_invite(token, -1, u_id)

def test_invalid_u_id():
    functions.general.clearDatabase()
    token = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")['token']
    channel_id = functions.channel.channels_create(token, "Pycharmers", True)['channel_id']
    with pytest.raises(ValueError):
        functions.channel.channel_invite(token, channel_id, -1)

def test_already_added():
    functions.general.clearDatabase()
    user_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    token = user_info['token']
    u_id = user_info['u_id']
    channel_id = functions.channel.channels_create(token, "Pycharmers", True)['channel_id']
    with pytest.raises(ValueError):
        functions.channel.channel_invite(token, channel_id, u_id)

def test_wrong_token_type():
    functions.general.clearDatabase()
    token = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")['token']
    u_id = functions.auth_functions.auth_register("tom@gmail.com", "password", "Tom", "Best")['u_id']
    channel_id = functions.channel.channels_create(token, "Pycharmers", True)['channel_id']
    with pytest.raises(TypeError):
        functions.channel.channel_invite(12345, channel_id, u_id)

def test_wrong_channel_id_type():
    functions.general.clearDatabase()
    token = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")['token']
    u_id = functions.auth_functions.auth_register("tom@gmail.com", "password", "Tom", "Best")['u_id']
    with pytest.raises(TypeError):
        functions.channel.channel_invite(token, "channel_id", u_id)

def test_wrong_u_id_type():
    functions.general.clearDatabase()
    token = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")['token']
    channel_id = functions.channel.channels_create(token, "Pycharmers", True)['channel_id']
    with pytest.raises(TypeError):
        functions.channel.channel_invite(token, channel_id, "u_id")

# test invited people inviting other people
# only people added by the creator of the channel are owners (as layed out in spec)
def test_invited_inviting():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    tom_info = functions.auth_functions.auth_register("tom@gmail.com", "password", "Tom", "Best")
    sam_info = functions.auth_functions.auth_register("sam@gmail.com", "password", "Sam", "Zest")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)['channel_id']
    functions.channel.channel_invite(bob_info['token'], channel_id, tom_info['u_id'])
    functions.channel.channel_invite(tom_info['token'], channel_id, sam_info['u_id'])
    channel_info = functions.channel.channel_details(bob_info['token'], channel_id)
    file = open("port.txt", "r")
    portNum = str(int(file.read()))
    bob_object = {"u_id": bob_info['u_id'], "name_first": "Bob",
                  "name_last": "Test", 'profile_img_url': 'http://localhost:' + portNum + '/static/default.png'}
    tom_object = {"u_id": tom_info['u_id'], "name_first": "Tom",
                  "name_last": "Best", 'profile_img_url': 'http://localhost:' + portNum + '/static/default.png'}
    sam_object = {"u_id": sam_info['u_id'], "name_first": "Sam",
                  "name_last": "Zest", 'profile_img_url': 'http://localhost:' + portNum + '/static/default.png'}

    assert bob_object in channel_info['owner_members']
    assert bob_object in channel_info['all_members']
    assert tom_object in channel_info['owner_members']
    assert tom_object in channel_info['all_members']
    assert sam_object not in channel_info['owner_members']
    assert sam_object in channel_info['all_members']

# test people who joined inviting other people
def test_joined_inviting():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    tom_info = functions.auth_functions.auth_register("tom@gmail.com", "password", "Tom", "Best")
    sam_info = functions.auth_functions.auth_register("sam@gmail.com", "password", "Sam", "Zest")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)['channel_id']
    functions.channel.channel_join(tom_info['token'], channel_id)
    functions.channel.channel_invite(tom_info['token'], channel_id, sam_info['u_id'])
    channel_info = functions.channel.channel_details(bob_info['token'], channel_id)
    file = open("port.txt", "r")
    portNum = str(int(file.read()))
    bob_object = {"u_id": bob_info['u_id'], "name_first": "Bob",
                  "name_last": "Test", 'profile_img_url': 'http://localhost:' + portNum + '/static/default.png'}
    tom_object = {"u_id": tom_info['u_id'], "name_first": "Tom",
                  "name_last": "Best", 'profile_img_url': 'http://localhost:' + portNum + '/static/default.png'}
    sam_object = {"u_id": sam_info['u_id'], "name_first": "Sam",
                  "name_last": "Zest", 'profile_img_url': 'http://localhost:' + portNum + '/static/default.png'}

    assert bob_object in channel_info['owner_members']
    assert bob_object in channel_info['all_members']
    assert tom_object not in channel_info['owner_members']
    assert tom_object in channel_info['all_members']
    assert sam_object not in channel_info['owner_members']
    assert sam_object in channel_info['all_members']

# test people not in the channel inviting people
def test_outsider_inviting():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    tom_info = functions.auth_functions.auth_register("tom@gmail.com", "password", "Tom", "Best")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)['channel_id']
    sam_info = functions.auth_functions.auth_register("sam@gmail.com", "password", "Sam", "Zest")
    with pytest.raises(ValueError):
        functions.channel.channel_invite(tom_info['token'], channel_id, sam_info['u_id'])

# being invited to a private channel
def test_private_invite():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    tom_info = functions.auth_functions.auth_register("tom@gmail.com", "password", "Tom", "Best")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", False)['channel_id']
    assert functions.channel.channel_invite(bob_info['token'], channel_id, tom_info['u_id']) == {}
    file = open("port.txt", "r")
    portNum = str(int(file.read()))
    bob_object = {"u_id": bob_info['u_id'], "name_first": "Bob",
                  "name_last": "Test", 'profile_img_url': 'http://localhost:' + portNum + '/static/default.png'}
    tom_object = {"u_id": tom_info['u_id'], "name_first": "Tom",
                  "name_last": "Best", 'profile_img_url': 'http://localhost:' + portNum + '/static/default.png'}
    member_list = [bob_object, tom_object]
    assert functions.channel.channel_details(bob_info['token'], channel_id) == {"name": "Pycharmers",
                                                              "owner_members": member_list,
                                                              "all_members": member_list}

def test_invalid_token():
    functions.general.clearDatabase()
    with pytest.raises(functions.errors.AccessError):
        functions.channel.channel_invite("token", 1, 1)