import os
import tornado.httpserver
import tornado.ioloop
import tornado.web
import math


# from tornado.options import define, options
# define("port", default=8000, help="run on the given port", type=int)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class MpgHandler(tornado.web.RequestHandler):
    def post(self):
        miles = float(self.get_argument('miles'))
        gallons = float(self.get_argument('gallons'))
        dollars = float(self.get_argument('dollars'))
        # self.render('mpg-results.html', miles=miles, gallons=gallons, dollars=dollars)
        self.render('mpg-results.html', m=miles, g=gallons, d=dollars)
    def get(self):
        self.render('mpg-calc.html')

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/*", MainHandler),
            (r"/mpg",MpgHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

def main():
    http_server = tornado.httpserver.HTTPServer(Application())
    port = int(os.environ.get("PORT", 5000))
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
