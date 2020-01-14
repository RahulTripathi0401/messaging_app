''' Tests for user_profile_setemail '''
import pytest

import functions.users
import functions.auth_functions
import functions.general
import functions.errors

def test_empty():
    functions.general.clearDatabase()
    with pytest.raises(functions.errors.AccessError):
        functions.users.user_profile_setemail("", "")

def test_empty_email():
    functions.general.clearDatabase()
    with pytest.raises(functions.errors.AccessError):
        functions.users.user_profile_setemail("token", "")

def test_type_token():
    functions.general.clearDatabase()
    with pytest.raises(TypeError):
        functions.users.user_profile_setemail(213423, "james@gmail.com")

def test_type_email():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    with pytest.raises(TypeError):
        functions.users.user_profile_setemail(bob_info['token'], 231432)

def test_invalid_email():
    functions.general.clearDatabase()
    token_return = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    with pytest.raises(ValueError):
        functions.users.user_profile_setemail(token_return["token"], "notvalid")

def test_used_email():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    functions.auth_functions.auth_register("james@gmail.com", "password", "james", "Test")
    with pytest.raises(ValueError):
        functions.users.user_profile_setemail(bob_info['token'], "james@gmail.com")

def test_valid_email_change():
    functions.general.clearDatabase()
    file = open("port.txt", "r")
    portNum = int(file.read())
    token_return = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    u_test = {'email': "bob@gmail.com", 'name_first': "Bob",
              'name_last': "Test", 'handle_str': "bobtest"
              , "profile_img_url": "http://localhost:" + str(portNum) + "/static/default.png", "u_id": 1}
    assert functions.users.user_profile(token_return['token'], token_return['u_id']) == u_test
    functions.users.user_profile_setemail(token_return['token'], "newbobemail@gmail.com")
    u_test = {'email': "newbobemail@gmail.com", 'name_first': "Bob",
              'name_last': "Test", 'handle_str': "bobtest",
              "profile_img_url": "http://localhost:" + str(portNum) + "/static/default.png", "u_id": 1}
    assert functions.users.user_profile(token_return['token'], token_return['u_id']) == u_test
