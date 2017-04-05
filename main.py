import os
import tornado.httpserver
import tornado.ioloop
from tornado.web import HTTPError
import tornado.web
import math
import textwrap
import psycopg2
import urlparse
import tornpsql

import handlers

class BaseHandler(tornado.web.RequestHandler):
    # checks current logged in user
    def get_current_user(self):
        return self.get_secure_cookie("userid")

class Application(tornado.web.Application):
    def __init__(self):
        routes = [
            (r"/", handlers.MainHandler),
            (r"/mpg",handlers.MpgHandler),
            (r"/mpg-view",handlers.MpgViewHandler),
            (r"/pi",handlers.PiHandler),
            (r"/login", handlers.LoginHandler),
            (r"/logout", handlers.LogoutHandler),
            (r"/signup", handlers.SignupHandler),
            (r"/.*", handlers.MainHandler),
        ]
        # connects to database
        self.db = tornpsql.Connection()

        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=(os.getenv("DEBUG")=='true'),
            cookie_secret=os.getenv("COOKIE_SECRET")
        )
        tornado.web.Application.__init__(self, routes, **settings)

def main():
    http_server = tornado.httpserver.HTTPServer(Application())
    port = int(os.getenv("PORT", 5000))
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
