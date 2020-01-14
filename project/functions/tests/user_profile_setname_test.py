''' Tests for functions.user.user_profile_setname '''
import pytest

import functions.users
import functions.auth_functions
import functions.general
import functions.errors

def test_empty():
    functions.general.clearDatabase()
    with pytest.raises(functions.errors.AccessError):
        functions.users.user_profile_setname("", "", "")

def test_type_token():
    functions.general.clearDatabase()
    with pytest.raises(TypeError):
        functions.users.user_profile_setname(213423, "James", "Last")

def test_type_name():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    with pytest.raises(TypeError):
        functions.users.user_profile_setname(bob_info['token'], 231432, 32232)

def test_type_name2():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    with pytest.raises(TypeError):
        functions.users.user_profile_setname(bob_info['token'], "231432", 32232)

def test_invalid_first_name():
    functions.general.clearDatabase()
    token_return = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    long_name = "nameoverfiftycharactersthatistoolongtobeconsideredvalid"
    with pytest.raises(ValueError):
        functions.users.user_profile_setname(token_return["token"], long_name, "Test")

def test_invalid_last_name():
    functions.general.clearDatabase()
    token_return = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    long_name = "nameoverfiftycharactersthatistoolongtobeconsideredvalid"
    with pytest.raises(ValueError):
        functions.users.user_profile_setname(token_return["token"], "Bob", long_name)

def test_valid_name_change():
    functions.general.clearDatabase()
    file = open("port.txt", "r")
    portNum = int(file.read())
    token_return = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    u_test = {'email': "bob@gmail.com", 'name_first': "Bob",
              'name_last': "Test", 'handle_str': "bobtest",
              "profile_img_url": "http://localhost:" + str(portNum) + "/static/default.png", "u_id": 1}
    assert functions.users.user_profile(token_return["token"], token_return["u_id"]) == u_test
    functions.users.user_profile_setname(token_return["token"], "validfirstname", "validlastname")
    u_test = {'email': "bob@gmail.com", 'name_first': "validfirstname",
              'name_last': "validlastname", 'handle_str': "bobtest", 
              "profile_img_url": "http://localhost:" + str(portNum) + "/static/default.png", "u_id": 1}
    assert functions.users.user_profile(token_return["token"], token_return["u_id"]) == u_test
