#!/usr/bin/env python
# encoding: utf-8
'''
融云 Server API Python 客户端
create by kitName
create datetime : 2016-09-05 
  
v2.0.1 
'''
import os
from rongcloud.user import User
from rongcloud.message import Message
from rongcloud.wordfilter import Wordfilter
from rongcloud.group import Group
from rongcloud.chatroom import Chatroom
from rongcloud.push import Push
from rongcloud.sms import SMS


class RongCloud:
    def __init__(self, app_key=None, app_secret=None):
        if app_key is None:
            app_key = os.environ.get('APP_KEY', '')
        if app_secret is None:
            app_secret = os.environ.get('APP_SECRET', '')
        self.User = User(app_key, app_secret)
        self.Message = Message(app_key, app_secret)
        self.Wordfilter = Wordfilter(app_key, app_secret)
        self.Group = Group(app_key, app_secret)
        self.Chatroom = Chatroom(app_key, app_secret)
        self.Push = Push(app_key, app_secret)
        self.SMS = SMS(app_key, app_secret)
