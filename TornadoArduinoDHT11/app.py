# -*- coding: utf-8 -*-

"""
A web monitor with Tornado web server enables real time plotting of DHT11 signals in the browser(support websocket)

License: this code is in the public domain

Author:   Cheng Tianshi
Email:    chengts95@163.com

Last modified: 2016.7.28
"""

import tornado.httpserver
import tornado.web
import tornado.websocket
import tornado.ioloop

import os

import json

from DHTSensor_monitor import *

clients = []

def checkSerial():
    t, phd = getTHD()
    for c in clients:
        c.write_message(json.dumps({'x': t, 'd0': float(
            phd['t']), 'd1': float(phd['h']), 'd2': float(phd['a'])}))

class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("index.html")

class WebSocketHandler(tornado.websocket.WebSocketHandler):

    def on_message(self, message):
        print("message received" + message)

    def open(self):
        clients.append(self)
        self.write_message(u"Connected")
        print("open")

    def on_close(self):
        clients.remove(self)
        print("close")

class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/websocket", WebSocketHandler),
        ]
        settings = {
            'template_path': os.path.join(os.path.dirname(__file__), "templates"),
            'static_path': os.path.join(os.path.dirname(__file__), "static")
        }
        
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == "__main__":

    openSerial()

    app = Application()
    appserver = tornado.httpserver.HTTPServer(app)
    appserver.listen(8000)

    mainLoop = tornado.ioloop.IOLoop.instance()
    # tornado.ioloop.PeriodicCallback(callback, callback_time, io_loop=None)
    # The callback is called every callback_time milliseconds.
    # Note that the timeout is given in milliseconds,
    scheduler = tornado.ioloop.PeriodicCallback(checkSerial, 2000, io_loop=mainLoop)

    scheduler.start()
    mainLoop.start()
