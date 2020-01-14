''' Tests for functions.channel.channel_removeowner '''
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
    functions.channel.channel_invite(bob_info['token'], channel_id, tom_info['u_id'])
    channel_info = functions.channel.channel_details(bob_info['token'], channel_id)
    file = open("port.txt", "r")
    portNum = int(file.read())
    assert {"u_id": tom_info['u_id'], "name_first": "Tom",
            "name_last": "Best", "profile_img_url": "http://localhost:" + str(portNum) + "/static/default.png"} in channel_info['owner_members']
    assert functions.channel.channel_removeowner(bob_info['token'], channel_id, tom_info['u_id']) == {}
    channel_info = functions.channel.channel_details(bob_info['token'], channel_id)

    assert {"u_id": tom_info['u_id'], "name_first": "Tom",
            "name_last": "Best", "profile_img_url": "http://localhost:" + str(portNum) + "/static/default.png"} not in channel_info['owner_members']

def test_invalid_channel_id():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    tom_info = functions.auth_functions.auth_register("tom@gmail.com", "password", "Tom", "Best")
    with pytest.raises(ValueError):
        functions.channel.channel_removeowner(bob_info['token'], -1, tom_info['u_id'])

def test_invalid_u_id():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)['channel_id']
    with pytest.raises(ValueError):
        functions.channel.channel_removeowner(bob_info['token'], channel_id, -1)

def test_invalid_token():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    tom_info = functions.auth_functions.auth_register("tom@gmail.com", "password", "Tom", "Best")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)['channel_id']
    functions.channel.channel_invite(bob_info['token'], channel_id, tom_info['u_id'])
    with pytest.raises(functions.errors.AccessError):
        functions.channel.channel_removeowner("badToken", channel_id, tom_info['u_id'])

def test_nonexistent_channel():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    tom_info = functions.auth_functions.auth_register("tom@gmail.com", "password", "Tom", "Best")
    with pytest.raises(ValueError):
        functions.channel.channel_addowner(bob_info['token'], 2534, tom_info['u_id'])

def test_wrong_token_type():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    tom_info = functions.auth_functions.auth_register("tom@gmail.com", "password", "Tom", "Best")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)['channel_id']
    functions.channel.channel_invite(bob_info['token'], channel_id, tom_info['u_id'])
    with pytest.raises(TypeError):
        functions.channel.channel_removeowner(12345, channel_id, tom_info['u_id'])

def test_wrong_channel_id_type():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    tom_info = functions.auth_functions.auth_register("tom@gmail.com", "password", "Tom", "Best")
    with pytest.raises(TypeError):
        functions.channel.channel_removeowner(bob_info['token'], "channel_id", tom_info['u_id'])

def test_wrong_u_id_type():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)['channel_id']
    with pytest.raises(TypeError):
        functions.channel.channel_removeowner(bob_info['token'], channel_id, "u_id")

# removing an owner without correct permission
def test_wrong_permissions():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    tom_info = functions.auth_functions.auth_register("tom@gmail.com", "password", "Tom", "Best")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)['channel_id']
    functions.channel.channel_join(tom_info['token'], channel_id)
    with pytest.raises(functions.errors.AccessError):
        functions.channel.channel_removeowner(tom_info['token'], channel_id, bob_info['u_id'])

# removing an owner when the person isnt actually an owner
def test_remove_nonowner():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    tom_info = functions.auth_functions.auth_register("tom@gmail.com", "password", "Tom", "Best")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)['channel_id']
    functions.channel.channel_join(tom_info['token'], channel_id)
    with pytest.raises(ValueError):
        functions.channel.channel_removeowner(bob_info['token'], channel_id, tom_info['u_id'])

# removing an owner when you arent in the channel
def test_outsider_removes():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    tom_info = functions.auth_functions.auth_register("tom@gmail.com", "password", "Tom", "Best")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)['channel_id']
    with pytest.raises(functions.errors.AccessError):
        functions.channel.channel_removeowner(tom_info['token'], channel_id, bob_info['u_id'])

# removing an owner when the u_id isnt in the channel
def test_outsider_removing():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    tom_info = functions.auth_functions.auth_register("tom@gmail.com", "password", "Tom", "Best")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)['channel_id']
    with pytest.raises(functions.errors.AccessError):
        functions.channel.channel_removeowner(bob_info['token'], channel_id, tom_info['u_id'])
