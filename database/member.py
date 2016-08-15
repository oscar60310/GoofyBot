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