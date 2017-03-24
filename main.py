import os
import tornado.httpserver
import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class MpgHandler(tornado.web.RequestHandler):
    def post(self):
        miles = self.get_argument('miles')
        gallons = self.get_argument('gallons')
        dollars = self.get_argument('dollars')
        self.render('mpg-results.html', miles=miles, gallons=gallons, dollars=dollars)
    def get(self):
        self.render('mpg-calc.html')

def main():
    application = tornado.web.Application([
        (r"/*", MainHandler),
        (r"/mpg*",MpgHandler),
    ])
    http_server = tornado.httpserver.HTTPServer(application)
    port = int(os.environ.get("PORT", 5000))
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
