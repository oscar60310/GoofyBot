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

import time
while True:
  time.sleep(10)
#twitch.stop()