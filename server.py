import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import uuid
import json
import time
from database.member import setting
class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        self.type = "none"
        self.login = 'false'
        
        self.id = uuid.uuid4()
        self.server.wss.append(self)
        self.server.msg('new connect - %s' % self.id)
        resp = {
            'uuid': str(self.id),
            'type': 'id'
        }
        self.write_message(resp);
       
    def on_message(self, message):
        self.server.rec(message,self)
    def on_close(self):
        self.server.msg('connection closed %s' % self.id)
        self.server.wss.remove(self)
    def check_origin(self, origin):
        return True
class serverControl():
  def __init__(self,cfg,twitch):
    self.wss = []
    self.WSHandler = WSHandler
    self.WSHandler.server = self
    self.cfg = cfg
    self.twitch = twitch
    twitch.web = self
  

  # start server
  def start_server(self):
    application = tornado.web.Application([
    (r'/ws', WSHandler),
    ])
    self.http_server = tornado.httpserver.HTTPServer(application)
    self.http_server.listen(10000)
    self.msg('Start listening')
    tornado.ioloop.IOLoop.instance().start()
  def msg(self,m):
    print '%s [WebScoket] %s' % (time.strftime("%b %d %Y %H:%M:%S"),m)

  #stop server
  def stop_server(self):
    tornado.ioloop.IOLoop.instance().stop()
    self.msg("server stop")
  #receive msg
  def rec(self,msg,ws):
    data = json.loads(msg)
    if data['type'] == 'login':
      if ws.type == 'none':
        from database.member import setting
        ws.setting = setting(self.cfg)
        ws.type = 'setting'

      #setting page login
      try:
        if ws.setting.logined:
          resp = {
            'code': 201,
            'description': "Has logined."
          }
          ws.write_message(resp)
        elif ws.setting.login(data['content']['user'],data['content']['pass'],ws.id):
          resp = {
            'code': 200,
            'description': "OK"
          }
          ws.write_message(resp)
          ws.user = data['content']['user']
          ws.login = 'true'
        else:
          resp = {
            'code': 403,
            'description': "Error password or username"
          }
          ws.write_message(resp)   
      except:
        self.msg('Id: %s login fail.' % ws.id)
        resp = {
            'code': 501,
            'description': "Login fail, client error."
        }
        ws.write_message(resp)
    #self.msg(data['type'])
    elif data['type'] == 'get_setting_data':
      if ws.login != 'true':
        resp = {
            'code': 401,
            'description': "Not login."
        }
        ws.write_message(resp)
      else:
        resp = {
            'code': 200,
            'description': "OK",
            'content': ws.setting.getdata()
        }
        ws.write_message(resp)
    elif data['type'] == 'token_login':
      ok = False
      try:
        ok = self.twitch.botroom.setting.token_check(data['user'],data['token'])
      except:
        ok = False
      if ok:
        self.twitch.send('JOIN #'+ data['user'] + '\n')
        ws.user = data['user']
        ws.type = 'room'
        resp = {
          'type': 'login',
          'code': 200,
          'description': "OK",
        }
        ws.write_message(resp)
      else:
        resp = {
          'type': 'login',
          'code': 403,
          'description': "password or username error",
        }
        ws.write_message(resp)