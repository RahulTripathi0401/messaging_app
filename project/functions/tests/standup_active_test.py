'''Tests for standup/active'''
import pytest
import datetime
import functions.auth_functions
import functions.standup
import functions.channel
import functions.general
import functions.errors

# wrong token type
# wrong channel_id type
# invalid token
# not a member
# not a channel
# no standup running
# standup running
# 30-60 second problems

def test_wrong_token_type():
    functions.general.clearDatabase()
    with pytest.raises(TypeError):
        functions.standup.standup_active(123, 1)

def test_wrong_channel_type():
    functions.general.clearDatabase()
    with pytest.raises(TypeError):
        functions.standup.standup_active("token", "channel")

def test_invalid_token():
    functions.general.clearDatabase()
    with pytest.raises(functions.errors.AccessError):
        functions.standup.standup_active("token", 1)

def test_not_in_channel():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@email.com", "password", "Bob", "Test")
    functions.channel.channels_create(bob_info['token'], 'Pycharmers', True)
    functions.channel.channel_leave(bob_info['token'], 1)
    with pytest.raises(functions.errors.AccessError):
        functions.standup.standup_active(bob_info['token'], 1)

def test_not_a_channel():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@email.com", "password", "Bob", "Test")
    with pytest.raises(ValueError):
        functions.standup.standup_active(bob_info['token'], 1)

def test_no_standup():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@email.com", "password", "Bob", "Test")
    functions.channel.channels_create(bob_info['token'], 'Pycharmers', True)
    assert functions.standup.standup_active(bob_info['token'], 1) == {'is_active': False, 'time_finish': None}

def test_standup():
    functions.general.clearDatabase()
    bob_info = functions.auth_functions.auth_register("bob@email.com", "password", "Bob", "Test")
    functions.channel.channels_create(bob_info['token'], 'Pycharmers', True)
    functions.general.set_time(functions.general.get_time())
    standup_return = functions.standup.standup_start(bob_info['token'], 1, 60)
    assert functions.standup.standup_active(bob_info['token'], 1) == {'is_active': True, 'time_finish': standup_return['time_finish']}
