# -*- coding: utf-8 -*-
from pymongo import MongoClient
class setting:
  def __init__(self,cfg):
    self.logined = False
    self.cfg = cfg
    self.client = MongoClient(cfg['db_ip'],cfg['db_port']).bot
    self.client.authenticate(cfg['db_user'],cfg['db_pass'])
    self.logined = False
  def login(self,user,password,id):
     if self.logined:
       return True
     userdatas = self.client.user.find({"name":user})
     if userdatas.count() == 0:
       return False
     else:
       currect = userdatas[0]['pass']
       import hashlib
       m = hashlib.md5()
       m.update(currect + str(id))
       currect = m.hexdigest()
       if currect == password:
         self.user = user
         self.logined = True
         return True
       else:
         return False
  def getdata(self):
    if self.logined:
      userdata = self.client.user.find({"name":self.user})[0]
      return userdata['data']
    else:
      return None
  def cleck_user(self,name):
    userdatas = self.client.user.find({"name":name})
    if userdatas.count() == 0:
      return False
    else:
      return True
  def register(self,name):
    self.client.user.insert_one({
      'name': name
    })
  def change_nick(self,who,twitchid,nick):
    
    try:
      nick_userdata = self.client.user.find({"name": who})[0]['data']['spe_name']
    except:
      self.client.user.update_one({"name": who},{"$set":{"data.spe_name":[]}})
      nick_userdata = self.client.user.find({"name": who})[0]['data']['spe_name']
    exist = False
    for nickdata in nick_userdata:
      if nickdata['name'] == twitchid:
        nickdata['nick'] = nick
        exist = True
        break
    if not exist:
      nick_userdata.append({
        'name': twitchid,
        'nick': nick
      })
    self.client.user.update_one({"name": who},{'$set':{'data.spe_name':nick_userdata}})
    return exist
  def rm_nick(self,who,twitch):
    try:
      nick_userdata = self.client.user.find({"name": who})[0]['data']['spe_name']
    except:
      self.client.user.update_one({"name": who},{"$set":{"data.spe_name":[]}})
      nick_userdata = self.client.user.find({"name": who})[0]['data']['spe_name']
    exist = False
    for i in xrange(len(nick_userdata)):
      if nick_userdata[i]['name'] == twitch:
        nick_userdata.pop(i)
        exist = True
        break
    self.client.user.update_one({"name": who},{'$set':{'data.spe_name':nick_userdata}})
    return exist
    