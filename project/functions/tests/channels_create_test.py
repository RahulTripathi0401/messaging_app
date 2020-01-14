''' Pytests written to test the 'channels_create' function '''
import pytest

import functions.channel
import functions.auth_functions
import functions.general
import functions.errors

def test_simple():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    chinfo = functions.channel.channels_create(bob_info['token'], "Pycharmers", True)
    assert 'channel_id' in chinfo
    assert functions.channel.channels_listall(bob_info['token']) == {"channels": [{"channel_id": chinfo['channel_id'],
                                                                 "name": "Pycharmers"}]}

def test_invalid_name():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    with pytest.raises(ValueError):
        functions.channel.channels_create(bob_info['token'], "reallylongnamethatisntallowed", True)

def test_wrong_token_type():
    functions.general.clearDatabase()
    with pytest.raises(TypeError):
        functions.channel.channels_create(12345, "name", True)

def test_invalid_token():
    functions.general.clearDatabase()
    with pytest.raises(functions.errors.AccessError):
        functions.channel.channels_create("token", "name", True)

def test_wrong_name_type():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    with pytest.raises(TypeError):
        functions.channel.channels_create(bob_info['token'], 12345, True)

def test_wrong_is_public_type():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    with pytest.raises(TypeError):
        functions.channel.channels_create(bob_info['token'], "name", 1)

def test_check_private():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    chinfo = functions.channel.channels_create(bob_info['token'], "Pycharmers", False)
    assert functions.channel.channels_listall(bob_info['token']) == {"channels": []}
    assert functions.channel.channels_list(bob_info['token']) == {"channels": [{"channel_id": chinfo['channel_id'],
                                                              "name": "Pycharmers"}]}

# Because flask reads all parameters as strings, the function needs to be able
# to convert string to boolean
def test_stringed_boolean():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    chinfo = functions.channel.channels_create(bob_info['token'], "Pycharmers", "False")
    assert functions.channel.channels_listall(bob_info['token']) == {"channels": []}
    assert functions.channel.channels_list(bob_info['token']) == {"channels": [{"channel_id": chinfo['channel_id'],
                                                              "name": "Pycharmers"}]}
    chinf2 = functions.channel.channels_create(bob_info['token'], "Pycharmers_Num2", "True")
    assert functions.channel.channels_listall(bob_info['token']) == {"channels": [{"channel_id": chinf2['channel_id'],
                                                                 "name": "Pycharmers_Num2"}]}
    assert functions.channel.channels_list(bob_info['token']) == {"channels": [{"channel_id": chinfo['channel_id'],
                                                              "name": "Pycharmers"},
                                                             {"channel_id": chinf2['channel_id'],
                                                              "name": "Pycharmers_Num2"}]}

def test_none_input():
    functions.general.clearDatabase()
    with pytest.raises(TypeError):
        functions.channel.channels_create(None, "name", True)

def test_bad_boolean():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    with pytest.raises(TypeError):
        functions.channel.channels_create(bob_info['token'], "name", "flatulent")
