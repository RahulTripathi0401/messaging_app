''' Pytests written to test the 'auth_login' function '''
import hashlib
import jwt
import pytest
import functions.auth_functions
import functions.helper_tokens
import functions.general

def test_simple_return():
    functions.general.clearDatabase()
    functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    hashed_pass = hashlib.sha256("password".encode()).hexdigest()
    token = jwt.encode({'u_id': 1, 'tokenNum': 1}, hashed_pass, algorithm='HS256').decode('utf-8')
    assert functions.auth_functions.auth_login("bob@gmail.com", "password") == {"u_id": 1, "token": token}

def test_empty():
    functions.general.clearDatabase()
    with pytest.raises(ValueError):
        functions.auth_functions.auth_login("", "")

def test_invalid_email():
    functions.general.clearDatabase()
    with pytest.raises(ValueError):
        functions.auth_functions.auth_login("notvalid", "password")

def test_unused_email():
    functions.general.clearDatabase()
    with pytest.raises(ValueError):
        functions.auth_functions.auth_login("notUsed@domain.com", "password")

def test_wrong_password():
    functions.general.clearDatabase()
    functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    with pytest.raises(ValueError):
        functions.auth_functions.auth_login("bob@gmail.com", "wrongpassword")

def test_wrong_type_email():
    functions.general.clearDatabase()
    with pytest.raises(TypeError):
        functions.auth_functions.auth_login(12345, "password")

def test_wrong_type_password():
    functions.general.clearDatabase()
    with pytest.raises(TypeError):
        functions.auth_functions.auth_login("valid@email.com", 12345)

# emails are still the same when capitalised so most email checks should be lower cased
def test_capital_simple():
    functions.general.clearDatabase()
    functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    hashed_pass = hashlib.sha256("password".encode()).hexdigest()
    token = jwt.encode({'u_id': 1, 'tokenNum': 1}, hashed_pass, algorithm='HS256').decode('utf-8')
    assert functions.auth_functions.auth_login("BOB@GMAIL.COM", "password") == {"u_id": 1, "token": token}

# Maybe unnecessary but checks that the function isn't authenticating a login with any valid
# password but rather only the password associated with a given email
def test_someoneelses_password():
    functions.general.clearDatabase()
    functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    functions.auth_functions.auth_register("tom@gmail.com", "tomspassword", "Tom", "Best")
    with pytest.raises(ValueError):
        functions.auth_functions.auth_login("bob@gmail.com", "tomspassword")

# Could test that the token and u_id being returned are valid and refers to the right account
def test_token_info():
    functions.general.clearDatabase()
    functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    test_return = functions.auth_functions.auth_login("bob@gmail.com", "password")
    assert functions.helper_tokens.tokenValidity(test_return["token"])
    assert functions.helper_tokens.tokenEmail(test_return["token"]) == "bob@gmail.com"
    assert functions.helper_tokens.token_u_id(test_return["token"]) == test_return["u_id"]

# Check if there is already a token for the user? might be able to store multiple
    # Can tokens be invalidated through methods other than auth_logout() being called?

# Check that the password is being stored case sensitively
def test_wrong_password_capitals():
    functions.general.clearDatabase()
    functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    with pytest.raises(ValueError):
        functions.auth_functions.auth_login("bob@gmail.com", "PASSWORD")
