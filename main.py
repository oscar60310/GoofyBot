# -*- coding: utf-8 -*-
print('BotGoofy start loading.')
#Load Config
config_file = open('./config.txt','r')
import json
cfg = json.loads(config_file.read())
config_file.close()

from irc.twitch import twitch
twitch = twitch(cfg)
# start twitch connect
twitch.start()

from server import serverControl
import threading

server = serverControl(cfg,twitch)
server_thread = threading.Thread(target = server.start_server)
server_thread.daemon = True 
server_thread.start()

import time
while True:
  time.sleep(10)
#twitch.stop()