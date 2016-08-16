# -*- coding: utf-8 -*-
import time
from database.member import setting 
class botroom:
  def __init__(self,twitch):
    self.twitch = twitch
    self.setting = setting(twitch.cfg)
  def command(self,msgs,who):
    #self.msg(msgs)
    if msgs == '!註冊' or msgs == "!register":
      if self.setting.cleck_user(who):
        self.whisper(who,'您已經註冊過了，您可以使用 !join 指令讓機器人加入您的聊天室')
      else:
        self.whisper(who,'ok')
  def msg(self,m):
    print '%s [BotRoom] %s' % (time.strftime("%b %d %Y %H:%M:%S"),m)
  def whisper(self, to ,m):
    self.twitch.send_to_room(self.twitch.botname,'/w %s %s' % (to,m))