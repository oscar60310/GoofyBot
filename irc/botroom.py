# -*- coding: utf-8 -*-
import time
from database.member import setting 
class botroom:
  def __init__(self,twitch):
    self.twitch = twitch
    self.setting = setting(twitch.cfg)
    
  def command(self,msgs,who):
    args = msgs.split(' ')
    #self.msg(msgs)
    if args[0] == '!註冊' or args[0] == "!register":
      if self.setting.cleck_user(who):
        self.whisper(who,'您已經註冊過了，您可以使用 !join 指令讓機器人加入您的聊天室')
      else:
        self.setting.register(who)
        self.whisper(who,'註冊完成，謝謝您的使用。您可以使用 !join 指令讓機器人加入您的聊天室')
        self.whisper(who,'所有指令都是由私訊傳送，請不要在聊天室中下指令喔 :)')
    elif self.check_reg(who):
      if args[0] == '!join':
        self.twitch.send('JOIN #'+ who + '\n')
        self.twitch.send_to_room(who,'哈囉，我加入這個聊天室了!')
        self.whisper(who,'成功加入聊天室，輸入 !leave 可以讓機器人離開')
      elif args[0] == '!leave':
        self.twitch.send('PART #'+ who + '\n')
        self.whisper(who,'我離開了聊天室，掰掰')
      elif args[0] == "!nick":
        if len(args) != 3:
          self.whisper(who,'!nick [Twitch ID] [暱稱]')
        else:
          if self.setting.change_nick(who,args[1],args[2]):
            self.whisper(who,'成功將 %s 的暱稱改為 %s' % (args[1],args[2]))
          else:
            self.whisper(who,'成功新增 %s 的暱稱為 %s' % (args[1],args[2]))
      elif args[0] == "!nickrm":
        if len(args) != 2:
          self.whisper(who,'!nickrm [Twitch id]')
        else:
          if self.setting.rm_nick(who,args[1]):
            self.whisper(who,'成功將 %s 的暱稱移除' % args[1])
          else:
            self.whisper(who,'%s 還沒有設定暱稱' % args[1])
      elif args[0] == "!say":
        if len(args) < 2:
          self.whisper(who,'!say [訊息]')
        else:
          if args[1][0] == '/':
            self.whisper(who,'不可以輸入指令喔')
          else:
            msg_to = ''
            for k in range(1,len(args)):
              msg_to += args[k] + " "
            self.whisper(who,'沒問題')
            self.twitch.send_to_room(who,msg_to)
      elif args[0] == "!room":
        token = self.setting.get_room_token(who)
        self.whisper(who,'http://goofydog.me/bot/room.html?%s!%s' % (who.replace(" ", ""),token))
      elif args[0] == "!設定暱稱":
        if len(args) != 2:
          self.whisper(who,'!設定暱稱 [開啟/關閉]')
        else:
          if args[1] == '開啟':
            self.setting.setEditNickInRoom(who,True)
            self.whisper(who,'開放觀眾自由修改暱稱')
          elif args[1] == "關閉":
            self.setting.setEditNickInRoom(who,False)
            self.whisper(who,'不開放觀眾自由修改暱稱')
          else:
            self.whisper(who,'!設定暱稱 [開啟/關閉]')
      elif args[0] == "!猜拳":
        if len(args) != 2:
          self.whisper(who,'!猜拳 [開啟/關閉]')
        else:
          if args[1] == '開啟':
            self.setting.setCanDo(who,'guess',True)
            self.whisper(who,'開放觀眾猜拳')
          elif args[1] == "關閉":
            self.setting.setCanDo(who,'guess',False)
            self.whisper(who,'不開放觀眾猜拳')
          else:
            self.whisper(who,'!猜拳 [開啟/關閉]')
  def msg(self,m):
    print '%s [BotRoom] %s' % (time.strftime("%b %d %Y %H:%M:%S"),m)
  def whisper(self, to ,m):
    self.twitch.send_to_room(self.twitch.botname,'/w %s %s' % (to,m))
  def check_reg(self,name):
    if self.setting.cleck_user(name):
      return True
    else:
      self.whisper(name,'您還沒有註冊，請先輸入 !註冊 來登記')
      return False