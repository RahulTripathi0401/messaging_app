''' Tests for user_profile '''
import pytest
import functions.users
import functions.auth_functions
import functions.helper_tokens
import functions.general
import functions.errors

def test_empty():
    functions.general.clearDatabase()
    with pytest.raises(TypeError):
        functions.users.user_profile("", "")

# test user id is valid and associated with a token
def test_valid_user():
    functions.general.clearDatabase()
    test_return = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    assert functions.helper_tokens.tokenValidity(test_return["token"])
    assert functions.helper_tokens.token_u_id(test_return["token"]) == test_return["u_id"]

# ValueError on invalid tokens and u_ids
def test_invalid_token():
    functions.general.clearDatabase()
    functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    with pytest.raises(functions.errors.AccessError):
        functions.users.user_profile("token", -1)

def test_invalid_token_type():
    functions.general.clearDatabase()
    with pytest.raises(TypeError):
        functions.users.user_profile(43142, -1)

# ValueError on invalid tokens and u_ids
def test_invalid_user_id():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    with pytest.raises(ValueError):
        functions.users.user_profile(bob_info['token'], 2)

# test expected return values
def test_simple_test():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    file = open("port.txt", "r")
    portNum = int(file.read())
    u_test = {'email': "bob@gmail.com", 'name_first': "Bob",
              'name_last': "Test", 'handle_str': "bobtest",
              "profile_img_url": "http://localhost:" + str(portNum) + "/static/default.png", "u_id": 1}
    assert functions.users.user_profile(bob_info['token'], bob_info['u_id']) == u_test

def test_new_user():
    functions.general.clearDatabase()
    token_return = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    functions.users.user_profile_sethandle(token_return["token"], "bobHandle")
    file = open("port.txt", "r")
    portNum = int(file.read())
    u_test = {'email': "bob@gmail.com", 'name_first': "Bob",
              'name_last': "Test", 'handle_str': "bobHandle",
              "profile_img_url": "http://localhost:" + str(portNum) + "/static/default.png", "u_id": 1}
    assert functions.users.user_profile(token_return["token"], token_return["u_id"]) == u_test
