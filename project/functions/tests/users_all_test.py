''' Tests for functions.users.users_all '''
import pytest
# from functions.users.users_all import functions.users.users_all
# from functions.auth_functions.auth_register import functions.auth_functions.auth_register
# from general import functions.general.clearDatabase
# from functions.errors import functions.errors.AccessError
import functions.users
import functions.auth_functions
import functions.general
import functions.errors

file = open("port.txt", "r")
portNum = str(int(file.read()))
DEFAULTURL = "http://localhost:" + portNum + "/static/default.png"

def test_empty():
    functions.general.clearDatabase()
    with pytest.raises(functions.errors.AccessError):
        functions.users.users_all("")

def test_invalid_token():
    functions.general.clearDatabase()
    with pytest.raises(functions.errors.AccessError):
        functions.users.users_all("token")

def test_type_token():
    functions.general.clearDatabase()
    with pytest.raises(TypeError):
        functions.users.users_all(123)

def test_regular():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@email.com", "password", "Bob", "Test")
    bob_profile = {"email": "bob@email.com", "name_first": "Bob", "name_last": "Test",
                   "handle_str": "bobtest", "profile_img_url": DEFAULTURL, "u_id": 1}
    assert functions.users.users_all(bob_info['token']) == {"users": [bob_profile]}

def test_many_users():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@email.com", "password", "Bob", "Test")
    bob_profile = {"email": "bob@email.com", "name_first": "Bob", "name_last": "Test",
                   "handle_str": "bobtest", "profile_img_url": DEFAULTURL, "u_id": 1}
    functions.auth_functions.auth_register("tom@email.com", "password", "Tom", "Best")
    tom_profile = {"email": "tom@email.com", "name_first": "Tom", "name_last": "Best",
                   "handle_str": "tombest", "profile_img_url": DEFAULTURL, "u_id": 2}
    functions.auth_functions.auth_register("sam@email.com", "password", "Sam", "Zest")
    sam_profile = {"email": "sam@email.com", "name_first": "Sam", "name_last": "Zest",
                   "handle_str": "samzest", "profile_img_url": DEFAULTURL, "u_id": 3}
    functions.auth_functions.auth_register("bob2@email.com", "password", "Bob", "Test")
    bob2_profile = {"email": "bob2@email.com", "name_first": "Bob", "name_last": "Test",
                    "handle_str": "bobtest0", "profile_img_url": DEFAULTURL, "u_id": 4}
    assert functions.users.users_all(bob_info['token']) == {"users": [bob_profile, tom_profile,
                                                      sam_profile, bob2_profile]}
