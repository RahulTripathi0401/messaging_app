''' Classes for the server '''
from datetime import datetime
import jwt
from server import portNum

class User:
    ''' Class to hold info about a user '''
    def __init__(self, email, password, name_first, name_last, handle, u_id):
        self.email = email
        self.password = password
        self.name_first = name_first
        self.name_last = name_last
        self.handle = handle
        self.u_id = u_id
        self.tokenNums = []
        self.tokenNum = 0
        self.permission_id = 3
        self.profile_img_url = "/static/default.png"

    def getDict(self):
        ''' Return dictionary for 'member' object '''
        return {"u_id": self.u_id,
                "name_first": self.name_first,
                "name_last": self.name_last,
                "profile_img_url": self.get_image_url()}

    def getUserDict(self):
        ''' Return dictionary for 'user' object '''
        return {"u_id": self.u_id,
                "email": self.email,
                "name_first": self.name_first,
                "name_last": self.name_last,
                "handle_str": self.handle,
                "profile_img_url": self.get_image_url()}

    def newToken(self):
        ''' Create a new token '''
        self.tokenNums.append(self.tokenNum)
        token = jwt.encode({'u_id': self.u_id, 'tokenNum': self.tokenNum},
                           self.password, algorithm='HS256').decode('utf-8')
        self.tokenNum += 1
        return token

    def invalidateToken(self, tokenNum):
        ''' Invalidate an old token '''
        for item in self.tokenNums:
            if item == tokenNum:
                self.tokenNums.remove(tokenNum)
                return True
        return False

    def get_image_url(self):
        ''' Get the url to a user profile image, using port number '''
        return "http://localhost:" + str(portNum) + self.profile_img_url

    def is_admin(self):
        ''' Check if a user is an admin of the slakr '''
        return self.permission_id == 2 or self.permission_id == 1

class Channel:
    ''' Class to hold info about a channel '''
    def __init__(self, channel_id, name, is_public, creator):
        self.channel_id = channel_id
        self.name = name
        self.is_public = is_public
        self.owners = {creator['u_id']: creator}
        self.members = {creator['u_id']: creator}
        self.messages = {}
        self.messageCount = 0
        self.standup_timer = None
        self.standup_length = None
        self.standup_messages = []
        self.creator = creator['u_id']

    def getDict(self):
        ''' Return dictionary for 'channel' object '''
        return {"channel_id": self.channel_id, "name": self.name}

    def isMember(self, user_id):
        ''' Check if a given user is a member of the channel '''
        if user_id in self.members:
            return True
        return False

    def isOwner(self, user_id):
        ''' Check if a given user is an owner of the channel '''
        if user_id in self.owners:
            return True
        return False

class Message:
    ''' Class to hold info about a message '''
    def __init__(self, message_id, message, u_id):
        self.message_id = message_id
        self.message = message
        self.sender = u_id
        self.reacts = {}
        self.timeCreated = datetime.now()
        self.is_pinned = False

    def getDict(self, u_id):
        ''' Return dictionary for 'message' object '''
        fix_time = self.timeCreated.timestamp()
        new_reacts = []
        for react in self.reacts:
            new_reacts.append(self.reacts[react].getDict(u_id))
        return {"message_id": self.message_id,
                "u_id": self.sender,
                "message": self.message,
                "time_created": fix_time,
                "reacts": new_reacts,
                "is_pinned": self.is_pinned}

class React:
    ''' Class to hold info about a react '''
    def __init__(self, react_id):
        self.react_id = react_id
        self.u_ids = []

    def isUserReact(self, u_id):
        ''' Check if a given user has reacted to the message '''
        if u_id in self.u_ids:
            return True
        return False

    def getDict(self, u_id):
        ''' Return dictionary for 'react' object '''
        return {"react_id": self.react_id,
                "u_ids": self.u_ids,
                "is_this_user_reacted": self.isUserReact(u_id)}
