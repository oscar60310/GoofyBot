print('BotGoofy start loading.')
#Load Config
config_file = open('config.txt','r')
import json
cfg = json.loads(config_file.read())
config_file.close()

from pymongo import MongoClient
client = MongoClient(cfg['db_ip'],cfg['db_port']).bot
client.authenticate(cfg['db_user'],cfg['db_pass'])

for user in client.user.find():
  print user['name'] 

import server
server.start_server()