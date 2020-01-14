''' Tests for functions.channel.channel_addowner '''
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
    functions.channel.channel_join(tom_info['token'], channel_id)
    channel_info = functions.channel.channel_details(bob_info['token'], channel_id)
    file = open("port.txt", "r")
    portNum = str(int(file.read()))
    assert {"u_id": tom_info['u_id'], "name_first": "Tom",
            "name_last": "Best", 'profile_img_url': 'http://localhost:' + portNum + '/static/default.png'} not in channel_info['owner_members']
    assert functions.channel.channel_addowner(bob_info['token'], channel_id, tom_info['u_id']) == {}
    channel_info = functions.channel.channel_details(bob_info['token'], channel_id)
    assert {"u_id": tom_info['u_id'], "name_first": "Tom",
            "name_last": "Best", 'profile_img_url': 'http://localhost:' + portNum + '/static/default.png'} in channel_info['owner_members']

def test_invalid_channel_id():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    tom_info = functions.auth_functions.auth_register("tom@gmail.com", "password", "Tom", "Best")
    with pytest.raises(ValueError):
        functions.channel.channel_addowner(bob_info['token'], -1, tom_info['u_id'])

def test_nonexistent_channel():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    tom_info = functions.auth_functions.auth_register("tom@gmail.com", "password", "Tom", "Best")
    with pytest.raises(ValueError):
        functions.channel.channel_addowner(bob_info['token'], 2534, tom_info['u_id'])

def test_invalid_u_id():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)['channel_id']
    with pytest.raises(ValueError):
        functions.channel.channel_addowner(bob_info['token'], channel_id, -1)

def test_invalid_token():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)['channel_id']
    with pytest.raises(functions.errors.AccessError):
        functions.channel.channel_addowner("badToken", channel_id, bob_info['u_id'])

def test_wrong_token_type():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    tom_info = functions.auth_functions.auth_register("tom@gmail.com", "password", "Tom", "Best")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)['channel_id']
    functions.channel.channel_join(tom_info['token'], channel_id)
    with pytest.raises(TypeError):
        functions.channel.channel_addowner(12345, channel_id, tom_info['u_id'])

def test_wrong_channel_id_type():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    tom_info = functions.auth_functions.auth_register("tom@gmail.com", "password", "Tom", "Best")
    with pytest.raises(TypeError):
        functions.channel.channel_addowner(bob_info['token'], "channel_id", tom_info['u_id'])

def test_wrong_u_id_type():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)['channel_id']
    with pytest.raises(TypeError):
        functions.channel.channel_addowner(bob_info['token'], channel_id, "u_id")

# trying to make someone who is already an owner an owner again
def test_double_owner():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    tom_info = functions.auth_functions.auth_register("tom@gmail.com", "password", "Tom", "Best")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)['channel_id']
    functions.channel.channel_invite(bob_info['token'], channel_id, tom_info['u_id'])
    file = open("port.txt", "r")
    portNum = str(int(file.read()))
    assert {"u_id": tom_info['u_id'], "name_first": "Tom",
            "name_last": "Best", 'profile_img_url': 'http://localhost:' + portNum + '/static/default.png'} in functions.channel.channel_details(bob_info['token'], channel_id)['owner_members']
    with pytest.raises(ValueError):
        functions.channel.channel_addowner(bob_info['token'], channel_id, tom_info['u_id'])

# trying to make someone not in the group an owner
def test_outsider_owner():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    tom_info = functions.auth_functions.auth_register("tom@gmail.com", "password", "Tom", "Best")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)['channel_id']
    file = open("port.txt", "r")
    portNum = str(int(file.read()))
    assert {"u_id": tom_info['u_id'], "name_first": "Tom",
            "name_last": "Best", 'profile_img_url': 'http://localhost:' + portNum + '/static/default.png'} not in functions.channel.channel_details(bob_info['token'],
                                                        channel_id)['all_members']
    with pytest.raises(functions.errors.AccessError):
        functions.channel.channel_addowner(bob_info['token'], channel_id, tom_info['u_id'])

# someone who isnt an owner trying to make someone an owner
def test_regular_owner_attempt():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    tom_info = functions.auth_functions.auth_register("tom@gmail.com", "password", "Tom", "Best")
    sam_info = functions.auth_functions.auth_register("sam@gmail.com", "password", "Sam", "Zest")
    channel_id = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)['channel_id']
    functions.channel.channel_join(tom_info['token'], channel_id)
    functions.channel.channel_join(sam_info['token'], channel_id)
    file = open("port.txt", "r")
    portNum = str(int(file.read()))
    assert {"u_id": tom_info['u_id'], "name_first": "Tom",
            "name_last": "Best", 'profile_img_url': 'http://localhost:' + portNum + '/static/default.png'} not in functions.channel.channel_details(bob_info['token'],
                                                        channel_id)['owner_members']
    assert {"u_id": sam_info['u_id'], "name_first": "Sam",
            "name_last": "Zest", 'profile_img_url': 'http://localhost:' + portNum + '/static/default.png'} not in functions.channel.channel_details(bob_info['token'],
                                                        channel_id)['owner_members']
    with pytest.raises(functions.errors.AccessError):
        functions.channel.channel_addowner(tom_info['token'], channel_id, sam_info['u_id'])
