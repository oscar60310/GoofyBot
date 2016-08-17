# -*- coding: utf-8 -*-
import random
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
      elif args[0] == '!猜拳':
        if not self.twitch.botroom.setting.cando(room,'guess'):
          return
        if len(args) != 2:
          self.twitch.send_to_room(room,":p")
          return
        com = random.choice(['石頭','剪刀','布'])
        if args[1] == '石頭' or args[1] == '剪刀' or args[1] == '布':
          if com == args[1]:
            self.twitch.send_to_room(room,'我出 %s ，平手QQ' % com)
          elif com == '石頭':
            self.guess(args[1] == '剪刀',com,room,confrom)
          elif com == '剪刀':
            self.guess(args[1] == '布',com,room,confrom)
          else:
            self.guess(args[1] == '石頭',com,room,confrom)
        else:
          self.twitch.send_to_room(room,"%s 有人作弊啦" % room)
  def guess(self,win,com,room,who):
    if win:
      self.twitch.send_to_room(room,'我出 %s ，輸了吧XD' % com)
    else:
      self.twitch.send_to_room(room,'我出 %s ，可惡...' % com)
      self.twitch.send_to_room(room,'/timeout %s 1' % who)