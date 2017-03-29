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


# from tornado.options import define, options
# define("port", default=8000, help="run on the given port", type=int)



class PiHandler(tornado.web.RequestHandler):
    def get(self):
        pi = str(math.pi)
        piLong = '3. ' + textwrap.fill('14159265358979323846264338327950288419716939937510582097494459230781640628620899862803482534211706798214808651328230664709384460955058223172535940812848111745028410270193852110555964462294895493038196',6)
        self.render("pi.html", piPython = pi, piLong = piLong)

class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        # userid = self.get_secure_cookie('userid')
        if self.current_user:
        # if userid:
            self.redirect('/')
        else:
            self.render("login.html")

    def post(self):
        email = self.get_argument('email')
        if '@' not in email:
            raise HTTPError(400, reason='Invalid email')

        password = self.get_argument('password')

        record = self.application.db.get("SELECT userid from users where username=%s and password=%s limit 1;",
                                         email, password)
        if record:
            self.set_secure_cookie(record['userid'], expires_days=30)
            self.redirect('/')
        else:
            raise HTTPError(401)


class MpgHandler(tornado.web.RequestHandler):
    def post(self):
        miles = float(self.get_argument('miles'))
        gallons = float(self.get_argument('gallons'))
        dollars = float(self.get_argument('dollars'))
        self.application.db.query("""INSERT INTO mpg (miles, gallons, dollars)
                                      VALUES (%s, %s, %s)""",
                                      miles, gallons, dollars
                                      )
        # self.render('mpg-results.html', miles=miles, gallons=gallons, dollars=dollars)
        self.render('mpg-results.html', m=miles, g=gallons, d=dollars)

    def get(self):
        self.render('mpg-calc.html')


class Application(tornado.web.Application):
    def __init__(self):
        routes = [
            (r"/", handlers.MainHandler),
            (r"/mpg",MpgHandler),
            (r"/pi",PiHandler),
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
