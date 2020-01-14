''' Pytests written to test the 'functions.auth_functions.auth_register' function '''
import hashlib
import jwt
import pytest
import functions.auth_functions
import functions.helper_tokens
import functions.general
import server

def test_empty():
    functions.general.clearDatabase()
    with pytest.raises(ValueError):
        functions.auth_functions.auth_register("", "", "", "")

def test_simple_return():
    functions.general.clearDatabase()
    hashed_pass = hashlib.sha256("password".encode()).hexdigest()
    token = jwt.encode({'u_id': 1, 'tokenNum': 0}, hashed_pass, algorithm='HS256').decode('utf-8')
    assert functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Builder") == {"u_id": 1,
                                                                            "token": token}

def test_invalid_email():
    functions.general.clearDatabase()
    with pytest.raises(ValueError):
        functions.auth_functions.auth_register("notvalid", "password", "John", "Smith")

def test_used_email():
    functions.general.clearDatabase()
    functions.auth_functions.auth_register("alreadyUsed@domain.com", "password", "Spongebob", "Squarepants")
    with pytest.raises(ValueError):
        functions.auth_functions.auth_register("alreadyUsed@domain.com", "password", "Patrick", "Star")

def test_invalid_password():
    functions.general.clearDatabase()
    with pytest.raises(ValueError):
        functions.auth_functions.auth_register("validemail@domain.com", "no", "Short", "Man")

def test_invalid_name_first():
    functions.general.clearDatabase()
    with pytest.raises(ValueError):
        functions.auth_functions.auth_register("email@domain.com", "password",
                      "thequickbrownfoxjumpsoverthelazydogistoolongofanametobeused", "name_last")

def test_invalid_name_last():
    functions.general.clearDatabase()
    with pytest.raises(ValueError):
        functions.auth_functions.auth_register("email@domain.com", "password", "name_first",
                      "thequickbrownfoxjumpsoverthelazydogistoolongofanametobeused")

def test_wrong_email_type():
    functions.general.clearDatabase()
    with pytest.raises(TypeError):
        assert functions.auth_functions.auth_register(12345, "password", "Bob", "Builder")

def test_wrong_password_type():
    functions.general.clearDatabase()
    with pytest.raises(TypeError):
        assert functions.auth_functions.auth_register("bob@gmail.com", 12345, "Bob", "Builder")

def test_wrong_name_first_type():
    functions.general.clearDatabase()
    with pytest.raises(TypeError):
        assert functions.auth_functions.auth_register("bob@gmail.com", "password", 12345, "Builder")

def test_wrong_name_last_type():
    functions.general.clearDatabase()
    with pytest.raises(TypeError):
        assert functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", 12345)

def test_token_info():
    functions.general.clearDatabase()
    test_return = functions.auth_functions.auth_register("boob@gmail.com", "password", "Bob", "Builder")
    assert functions.helper_tokens.tokenValidity(test_return["token"])
    assert functions.helper_tokens.tokenEmail(test_return["token"]) == "boob@gmail.com"
    assert functions.helper_tokens.token_u_id(test_return["token"]) == test_return["u_id"]
    assert functions.helper_tokens.tokenNames(test_return["token"]) == ("Bob", "Builder")

# could do more scrupulous checks on password safety
    # probably a frontend problem

# check for whitespace in any fields - specifically at the beginning and end of
# names and anywhere in password
    # .strip()
    # wait until further spec updates before testing it

# maybe check the email gets stored in a lower case form if we want to do that
    # doesnt really matter how it's stored as long as it gets changed for the checks
def test_lower_case_email():
    functions.general.clearDatabase()
    test_return = functions.auth_functions.auth_register("BOAB@GMAIL.COM", "password", "Bob", "Builder")
    assert functions.helper_tokens.tokenValidity(test_return["token"])
    assert functions.helper_tokens.tokenEmail(test_return["token"]) == "boab@gmail.com"
    hashed_pass = hashlib.sha256("password".encode()).hexdigest()
    token = jwt.encode({'u_id': test_return['u_id'], 'tokenNum': 1},
                       hashed_pass, algorithm='HS256').decode('utf-8')
    assert functions.auth_functions.auth_login("boab@gmail.com", "password") == {"u_id": test_return['u_id'], "token": token}

def test_same_name():
    functions.general.clearDatabase()
    test_return = functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Builder")
    assert functions.helper_tokens.tokenHandle(test_return['token']) == "bobbuilder"
    test_return2 = functions.auth_functions.auth_register("boob@gmail.com", "password", "Bob", "Builder")
    assert functions.helper_tokens.tokenHandle(test_return2['token']) == "bobbuilder0"

def test_long_same_name():
    functions.general.clearDatabase()
    assert functions.helper_tokens.tokenHandle(functions.auth_functions.auth_register("bob@gmail.com", "password", "ReallyLongFirstName",
                                     "FollowedByAReallyLong")['token']) == "reallylongfirstnamef"
    assert functions.helper_tokens.tokenHandle(functions.auth_functions.auth_register("bab@gmail.com", "password", "ReallyLongFirstName",
                                     "FollowedByAReallyLong")['token']) == "reallylongfirstname0"
    assert functions.helper_tokens.tokenHandle(functions.auth_functions.auth_register("bbb@gmail.com", "password", "ReallyLongFirstName",
                                     "FollowedByAReallyLong")['token']) == "reallylongfirstname1"
    assert functions.helper_tokens.tokenHandle(functions.auth_functions.auth_register("bcb@gmail.com", "password", "ReallyLongFirstName",
                                     "FollowedByAReallyLong")['token']) == "reallylongfirstname2"
    assert functions.helper_tokens.tokenHandle(functions.auth_functions.auth_register("bdb@gmail.com", "password", "ReallyLongFirstName",
                                     "FollowedByAReallyLong")['token']) == "reallylongfirstname3"
    assert functions.helper_tokens.tokenHandle(functions.auth_functions.auth_register("beb@gmail.com", "password", "ReallyLongFirstName",
                                     "FollowedByAReallyLong")['token']) == "reallylongfirstname4"
    assert functions.helper_tokens.tokenHandle(functions.auth_functions.auth_register("bfb@gmail.com", "password", "ReallyLongFirstName",
                                     "FollowedByAReallyLong")['token']) == "reallylongfirstname5"
    assert functions.helper_tokens.tokenHandle(functions.auth_functions.auth_register("bgb@gmail.com", "password", "ReallyLongFirstName",
                                     "FollowedByAReallyLong")['token']) == "reallylongfirstname6"
    assert functions.helper_tokens.tokenHandle(functions.auth_functions.auth_register("bhb@gmail.com", "password", "ReallyLongFirstName",
                                     "FollowedByAReallyLong")['token']) == "reallylongfirstname7"
    assert functions.helper_tokens.tokenHandle(functions.auth_functions.auth_register("bib@gmail.com", "password", "ReallyLongFirstName",
                                     "FollowedByAReallyLong")['token']) == "reallylongfirstname8"
    assert functions.helper_tokens.tokenHandle(functions.auth_functions.auth_register("bjb@gmail.com", "password", "ReallyLongFirstName",
                                     "FollowedByAReallyLong")['token']) == "reallylongfirstname9"
    assert functions.helper_tokens.tokenHandle(functions.auth_functions.auth_register("bkb@gmail.com", "password", "ReallyLongFirstName",
                                     "FollowedByAReallyLong")['token']) == "reallylongfirstnam10"
    assert functions.helper_tokens.tokenHandle(functions.auth_functions.auth_register("blb@gmail.com", "password", "ReallyLongFirstName",
                                     "FollowedByAReallyLong")['token']) == "reallylongfirstnam11"

def test_slackr_god():
    functions.general.clearDatabase()
    functions.auth_functions.auth_register("bob@gmail.com", "password", "Bob", "Test")
    assert server.users[1].permission_id == 1
