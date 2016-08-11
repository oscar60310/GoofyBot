import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import uuid
import json
class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        self.id = uuid.uuid4()
        wss.append(self)
        msg('new connect - %s' % self.id)
        self.write_message(str(self.id));
    def on_message(self, message):
        rec(self,message)
    def on_close(self):
        msg('connection closed')
        wss.remove(self)
    def check_origin(self, origin):
        return True
application = tornado.web.Application([
    (r'/ws', WSHandler),
])
http_server = []
wss = []
def rec(ws,msg):
  try:
    data = json.loads(msg)
    print(data['type'])
  except:
    msg('Kick error connect %s' % ws.id)
    ws.close()
    ws = []

def msg(m):
  print '[WebScoket] %s' % m
def start_server():
  http_server = tornado.httpserver.HTTPServer(application)
  http_server.listen(10000)

  msg('Start listening')
  tornado.ioloop.IOLoop.instance().start()
def stop_server():
  tornado.ioloop.IOLoop.instance().stop()
  msg("server stop")
