# Assumptions

## General
That we should raise TypeErrors whenever given an incorrect type

Probably need to check validity of token anywhere a token is given
    functions can pull those details out of a token, otherwise the token won't do anything

We can store multiple tokens in case the users want to be logged in from multiple devices at once

Each test should probably be performed on an empty database so we can/should be registering our own users and calling other functions relevant to our tests

## auth_register, auth_login
Emails will be stored as lower cased so users can log in even if when they signed up they used a valid email with any capitalisation

Once a user is created they will automatically be logged in

## auth_passwordreset_request
In line with spec but not checking whether email is actually linked to an account as a general security thing
Assumption that giving an invalid email should raise a ValueError

## auth_passwordreset_reset
Assume that if the function is called without a prior request it just returns a valid Error

## message_send
Assume that the message_id is correct is there is no way to retrieve it

## channel_invite
Assume that a user can't invite a user already part of a channel to it and that it would raise a ValueError
Assume that any member of a channel can invite someone else into it, regardless of permissions
Assume that if a user not in a channel tries to invite someone into it the function raises an AccessError
In line with the spec but only people added by the creator of the channel are owners, not those added by other owners

## channels_create
Assume that the person creating the channel is automatically added to the channel

## channel_messages
Assume that the message IDs are unique to their given channel

## channel_leave
Assume that if the token is associated with a user not in the channel, raise an AccessError

## channel_join
Assume that you can't join non-public channels, only be invited
    raise an AccessError

## channel_addowner
Assume that if the u_id isn't linked to an account, raise a ValueError

## search
Assume that a search query cannot be longer than 40 characters

## admin_userpermission_change
Assume that there is a way to tell what type of permissions a user has from their user ID or token in order to determine whether:
A) A regular member is trying to become an admin or owner (which is not permitted)
B) An admin is trying to become an admin, an owner an owner, etc.

The token in the admin_userpermission_change function refers to the token of the user who is trying to change the userpermission and the uid is
of the user whose permissions they are trying to change whether it is themselves or another user.

A channel must always have an owner but an owner can change own status from owner to admin as long as there is another owner.

## standup_start
You must be a channel member to start a standup in that channel

You cannot start a standup in a channel when one is already running

## standup send
Assume that current time can be determined using two functions that have not yet been implemented
1) gettime() which finds the current time and
2) settime() which sets the time to a desired time

## message_sendlater
Assumes that the channel is initially empty when sending the message later.
Assumes that the datetime.now() provides the current time
Assumes that timedelta can shift the time in specified increments
Assumes that the tokens provided are valid

## message_send
Assumes that the channel is initially empty when sending the message later.
Assumes that the token provided is valid
Assumes that the channel_id provided is valid

## message_remove
Assumes that the message removed from the channel is automatically removed

## message_edit
Assumes that the contents of the message are removed and then replaced

## message_react
Assume that if the token isn't valid, raise an AccessError if you aren't in the channel or the message doesnt belong to you
That the channel_id can be pulled from the associated message_id

## message_unreact
Assume that if the token isn't valid, raise an AccessError if you aren't in the channel or the message doesnt belong to you
That the channel_id can be pulled from the associated message_id

## message_pin
Assume that if the token provided is valid
Assumes that the messaged can be pinned by the ownwer as well as the admin
Assumes that multiple messages can be pinned

## message_unpin
Assume that if the token provided is valid
Assumes that the messaged can be pinned by the ownwer as well as the admin
Assumes that multiple messages can be unpinned

## user_profiles_uploadphoto_test
Assume given image used in testing has dimensions of 100 by 100
