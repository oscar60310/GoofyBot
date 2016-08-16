# -*- coding: utf-8 -*-
print('BotGoofy start loading.')
#Load Config
config_file = open('config.txt','r')
import json
cfg = json.loads(config_file.read())
config_file.close()

from irc.twitch import twitch
twitch = twitch(cfg)
# start twitch connect
twitch.start()
while True:
  com = raw_input("")
  if com == 'q':
    twitch.stop()
    break