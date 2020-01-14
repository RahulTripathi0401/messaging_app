''' Pytests written to test the 'channels_listall' function '''
import pytest

import functions.channel
import functions.auth_functions
import functions.general
import functions.errors

def test_simple():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    channel_id1 = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)['channel_id']
    channel_id2 = functions.channel.channels_create(bob_info['token'], "Pycharmers2", True)['channel_id']
    assert functions.channel.channels_listall(bob_info['token']) == {"channels": [{"channel_id": channel_id1,
                                                                 "name": "Pycharmers"},
                                                                {"channel_id": channel_id2,
                                                                 "name": "Pycharmers2"}]}

def test_wrong_token_type():
    with pytest.raises(TypeError):
        functions.channel.channels_listall(12345)

def test_invalid_token():
    with pytest.raises(functions.errors.AccessError):
        functions.channel.channels_listall("token")

# empty list test
def test_empty():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    assert functions.channel.channels_listall(bob_info['token']) == {"channels": []}

# doesnt list private channels
def test_private():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    channel_id1 = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)['channel_id']
    functions.channel.channels_create(bob_info['token'], "Pycharmers2", False)
    assert functions.channel.channels_listall(bob_info['token']) == {"channels": [{"channel_id": channel_id1,
                                                                 "name": "Pycharmers"}]}

# list all channels whether or not you're a part of it
def test_not_in():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    channel_id1 = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)['channel_id']
    channel_id2 = functions.channel.channels_create(bob_info['token'], "Pycharmers2", True)['channel_id']
    functions.channel.channel_leave(bob_info['token'], channel_id2)
    assert functions.channel.channels_listall(bob_info['token']) == {"channels": [{"channel_id": channel_id1,
                                                                 "name": "Pycharmers"},
                                                                {"channel_id": channel_id2,
                                                                 "name": "Pycharmers2"}]}
