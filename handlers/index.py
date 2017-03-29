import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):

        records=self.application.db.query("SELECT * FROM mpg")
        self.render("index.html", records=records)
        # self.write(":)")
