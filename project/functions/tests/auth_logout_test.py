''' Pytests written to test the 'functions.auth_functions.auth_logout' function '''
import hashlib
import pytest
import functions.auth_functions
import functions.helper_tokens
import functions.general

def test_simple_return():
    functions.general.clearDatabase()
    token = functions.auth_functions.auth_register("bob@gmail.com", "testpassword", "Bob", "Test")['token']
    assert functions.auth_functions.auth_logout(token) == {"is_success": True}

def test_wrong_token_type():
    functions.general.clearDatabase()
    with pytest.raises(TypeError):
        functions.auth_functions.auth_logout(12345)

# test that the token being given is invalidated
def test_token_invalidated():
    functions.general.clearDatabase()
    token = functions.auth_functions.auth_register("bob@gmail.com", "testpassword", "Bob", "Test")['token']
    assert functions.helper_tokens.tokenValidity(token)
    assert functions.auth_functions.auth_logout(token) == {"is_success": True}
    assert not functions.helper_tokens.tokenValidity(token)

# could check that nothing happens if the token is invalid
def test_useless_token():
    functions.general.clearDatabase()
    assert not functions.helper_tokens.tokenValidity("fakeToken")
    assert functions.auth_functions.auth_logout("fakeToken") == {"is_success": False}
    assert not functions.helper_tokens.tokenValidity("fakeToken")
    # could add other checks on data

# only invalidate the provided token
    # if we're storing multiple tokens in case the user is logged in on multiple devices
def test_single_invalidation():
    functions.general.clearDatabase()
    token1 = functions.auth_functions.auth_register("bob@gmail.com", "testpassword", "Bob", "Test")['token']
    token2 = functions.auth_functions.auth_login("bob@gmail.com", "testpassword")['token']
    assert functions.helper_tokens.tokenValidity(token1)
    assert functions.helper_tokens.tokenValidity(token2)
    assert functions.auth_functions.auth_logout(token1) == {"is_success": True}
    assert not functions.helper_tokens.tokenValidity(token1)
    assert functions.helper_tokens.tokenValidity(token2)
