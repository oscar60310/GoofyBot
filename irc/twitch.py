# -*- coding: utf-8 -*-
import socket 
import time
import threading
from irc.botroom import botroom
class twitch:
  def __init__(self,cfg):
    self.cfg = cfg
    self.active = True 
    self.timer = 0
    self.msg_sended = 0
    self.botname = cfg['bot_name']
    self.botroom = botroom(self)
  def msg(self,m):
    print '%s [Twitch] %s' % (time.strftime("%b %d %Y %H:%M:%S"),m)
  def connect(self):
    #try:
      self.msg('try to connect twitch server.')
      self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.client.connect(("irc.chat.twitch.tv", 6667))
      self.msg('twitch server connected.')
      # start receive tread
      self.recv_thread = threading.Thread(target = self.recv_func)
      self.recv_thread.daemon = True 
      self.recv_thread.start()
      # start send msg timer
      self.timer_thread = threading.Thread(target = self.limit_time)
      self.timer_thread.daemon = True 
      self.timer_thread.start()
      # login
      self.send('PASS ' + self.cfg['bot_pass'] + '\n')
      self.send('NICK ' + self.cfg['bot_name'] + '\n')
      self.send('JOIN #'+ self.cfg['bot_name'] + '\n')
      self.send('CAP REQ :twitch.tv/commands\n')
      # Welcome msg
      self.send_to_room(self.botname,'Bot service connected.')
      return True
    #except:
     # return False
  def start(self):
    while not self.connect() and self.active:
      self.msg('connect fail, try again in 5 seconds.')
      time.sleep(5)
  def stop(self):
    self.active = False
    self.msg('shut down connect between twitch server...')
    self.client.shutdown(socket.SHUT_RDWR)
    self.client.close()
  def recv(self):
    tmp = ""
    chunk = self.client.recv(225) 
    tmp += chunk
    if tmp.find('\n') != -1: 
      ss = tmp.split('\n')
      for ns in range(len(ss)-1):
        self.msg(ss[ns][0:len(ss[ns])-1])
        self.handle_msg(ss[ns][0:len(ss[ns])-1])
      tmp = ss[len(ss)-1]
  def recv_func(self):
    self.msg('start receive message.')
    while self.active:
      self.recv()
    self.msg('stop receive message.')
  def limit_time(self):
    self.msg('start message timer.')
    while self.active:
      self.timer += 1
      if self.timer >= 30:
        self.msg_sended = 0
        self.timer = 0
      time.sleep(1)
    self.msg('stop message timer.')
  def send(self,msgs):
    while self.msg_sended > 15:
      self.msg('too many message, waitting...')
      time.sleep(1)
    self.msg_sended += 1
    self.client.sendall(msgs)
    #self.msg(' [send] ' + msgs)
  def handle_msg(self,msgs):
    if msgs == "PING :tmi.twitch.tv":
      self.msg('respond ping request.')
      self.send('PONG :tmi.twitch.tv\n')
    elif msgs.split(' ')[1] == "PRIVMSG":
      # user message
      sendFrom = msgs.split(' ')[0].split('!')[0].split(':')[1]
      sendTo = msgs.split(' ')[2].split('#')[1]
      msg_data = ""
      data = msgs.split(':')
      for k in range(2,len(data)):
        msg_data += data[k]
      if sendTo == self.botname:
        # sendTO bot chat room
        if msg_data[0] == '!':
          self.send_to_room(self.botname,sendFrom + ' 請使用私訊方式(/w botgoofy [指令])來執行指令喔')
          self.send_to_room(self.botname,"/timeout %s 1" % sendFrom)
    elif msgs.split(' ')[1] == "WHISPER":
      # user WHISPER
      sendFrom = msgs.split(' ')[0].split('!')[0].split(':')[1]
      msg_data = ""
      data = msgs.split(':')
      for k in range(2,len(data)):
        msg_data += data[k]
      if msg_data[0] == '!':
         self.botroom.command(msg_data,sendFrom)  
  def send_to_room(self,room,msgs):
    self.send('PRIVMSG #{0} :{1}\n'.format(room,msgs))
  
      
