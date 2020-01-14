''' Tests for user_profile_sethandle '''
import pytest
import functions.users
import functions.auth_functions
import functions.errors
import functions.general

def test_empty():
    functions.general.clearDatabase()
    with pytest.raises(functions.errors.AccessError):
        functions.users.user_profile_sethandle("", "")

def test_invalid_handle():
    functions.general.clearDatabase()
    token_return = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    with pytest.raises(ValueError):
        functions.users.user_profile_sethandle(token_return["token"], "invaliduserhandleover20characterslong")

def test_type_token():
    functions.general.clearDatabase()
    with pytest.raises(TypeError):
        functions.users.user_profile_sethandle(213423, "coolhandle")

def test_type_handle():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    with pytest.raises(TypeError):
        functions.users.user_profile_sethandle(bob_info['token'], 231432)

def test_valid_handle_change():
    functions.general.clearDatabase()
    file = open("port.txt", "r")
    portNum = int(file.read())
    token_return = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    functions.users.user_profile_sethandle(token_return["token"], "bobHandle")
    u_test = {'email': "bob@gmail.com", 'name_first': "Bob",
              'name_last': "Test", 'handle_str': "bobHandle",
              "profile_img_url": "http://localhost:" + str(portNum) + "/static/default.png", "u_id": 1}
    assert functions.users.user_profile(token_return["token"], token_return["u_id"]) == u_test
