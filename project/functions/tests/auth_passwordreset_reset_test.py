''' Pytests written to test the 'functions.auth_functions.auth_passwordreset_reset' function '''
import hashlib
import pytest
import functions.auth_functions
import functions.general
import functions.tests.auth_passwordreset_request_test
import server

def test_simple_return():
    functions.general.clearDatabase()
    functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    server.users[1].reset_code = hashlib.sha256("AAAAAA".encode()).hexdigest()
    assert functions.auth_functions.auth_passwordreset_reset("AAAAAA", "newpassword") == {}

def test_wrong_reset_code():
    functions.general.clearDatabase()
    functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    functions.auth_functions.auth_passwordreset_request("bob@gmail.com")
    with pytest.raises(ValueError):
        functions.auth_functions.auth_passwordreset_reset("wrong", "password")

def test_invalid_password():
    functions.general.clearDatabase()
    functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    server.users[1].reset_code = hashlib.sha256("AAAAAA".encode()).hexdigest()
    with pytest.raises(ValueError):
        functions.auth_functions.auth_passwordreset_reset("AAAAAA", "bad")

def test_reset_code_wrong_type():
    functions.general.clearDatabase()
    functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    functions.auth_functions.auth_passwordreset_request("bob@gmail.com")
    with pytest.raises(TypeError):
        functions.auth_functions.auth_passwordreset_reset(12345, "password")

def test_new_password_wrong_type():
    functions.general.clearDatabase()
    functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    functions.auth_functions.auth_passwordreset_request("bob@gmail.com")
    with pytest.raises(TypeError):
        functions.auth_functions.auth_passwordreset_reset("correct", 12345)

# Raise a valueError if the function is called when there isn't any associated resetcode
def test_no_reset_code():
    functions.general.clearDatabase()
    functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    assert not functions.tests.auth_passwordreset_request_test.helper_resetcode_exists("bob@gmail.com")
    with pytest.raises(ValueError):
        functions.auth_functions.auth_passwordreset_reset("wrong", "password")
