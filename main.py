# -*- coding: utf-8 -*-
print('BotGoofy start loading.')
#Load Config
config_file = open('config.txt','r')
import json
cfg = json.loads(config_file.read())
config_file.close()

#from pymongo import MongoClient
#client = MongoClient(cfg['db_ip'],cfg['db_port']).bot
#client.authenticate(cfg['db_user'],cfg['db_pass'])

#for user in client.user.find():
#  print user['name'] 

# web socket server
from server import serverControl
server = serverControl(cfg)
def server_go():
  server.start_server()
# start web socket
import threading
server_thread = threading.Thread(target = server_go)
server_thread.daemon = True 
server_thread.start()
while True:
  com = raw_input("")
  if com == 'q':
    server.stop_server()
    break