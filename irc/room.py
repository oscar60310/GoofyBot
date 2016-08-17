# -*- coding: utf-8 -*-
class room:
  def __init__(self,twitch):
    self.twitch = twitch
  def handle_msg(self,room,confrom,msgs):
    if msgs[0] == '!':
      args = msgs.split(' ')
      if args[0] == '!暱稱':
        if len(args) != 2:
          self.twitch.send_to_room(room,"!暱稱 [你想要的名子]")
          return
        if self.twitch.botroom.setting.canEditNickInRoom(room):
          self.twitch.botroom.setting.change_nick(room,confrom,args[1])
          self.twitch.send_to_room(room,"Hi %s，我記得你了!" % args[1])
        else:
          self.twitch.send_to_room(room,"這個聊天室目前不開放自由修改暱稱喔")
  