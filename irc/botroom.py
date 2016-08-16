# -*- coding: utf-8 -*-
import time
class botroom:
  def __init__(self,twitch):
    self.twitch = twitch
  def command(self,msgs,who):
    #self.msg(msgs)
    if msgs == '!註冊' or msgs == "!register":
      self.whisper(who,'ok')
  def msg(self,m):
    print '%s [BotRoom] %s' % (time.strftime("%b %d %Y %H:%M:%S"),m)
  def whisper(self, to ,m):
    self.twitch.send_to_room(self.twitch.botname,'/w %s %s' % (to,m))