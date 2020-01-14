''' Pytests written to test the 'functions.auth_functions.auth_passwordreset_request' function '''
import pytest
import functions.auth_functions
import functions.general
import server

def test_simple_return():
    functions.general.clearDatabase()
    functions.auth_functions.auth_register("valid@email.com", "password", "Valid", "Person")
    assert functions.auth_functions.auth_passwordreset_request("valid@email.com") == {}

# shouldnt raise flags if email is invalid
    # find a way to make sure email wasn't sent?
def test_invalid_email():
    functions.general.clearDatabase()
    assert functions.auth_functions.auth_passwordreset_request("invalid") == {}

def test_wrong_email_type():
    functions.general.clearDatabase()
    with pytest.raises(TypeError):
        functions.auth_functions.auth_passwordreset_request(12345)

# check that an email is sent and code generated if the email is associated with an account
def test_code_exists():
    functions.general.clearDatabase()
    functions.auth_functions.auth_register("valid@email.com", "password", "Valid", "Person")
    assert not helper_resetcode_exists("valid@email.com")
    functions.auth_functions.auth_passwordreset_request("valid@email.com")
    assert helper_resetcode_exists("valid@email.com")

# check that nothing happens if the email is not associated with an account
def test_code_doesnt_exist():
    functions.general.clearDatabase()
    functions.auth_functions.auth_passwordreset_request("fake@email.com")
    assert not helper_resetcode_exists("fake@email.com")
    # should probably check more of the database

# Helper function that checks whether there is an associated reset code with a given email
def helper_resetcode_exists(email):
    for key in server.users:
        if server.users[key].email == email:
            if hasattr(server.users[key], 'reset_code'):
                return True
    return False
