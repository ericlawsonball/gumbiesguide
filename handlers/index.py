import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        # records=self.application.db.query("SELECT * FROM mpg")
        firstName = ""
        flagLoggedIn = False
        userid = self.get_secure_cookie('userid')
        if userid:
            userid = tornado.escape.xhtml_escape(self.get_secure_cookie('userid'))
            record = self.application.db.get("""SELECT first_name
                                                 FROM users
                                                 WHERE userid=%s
                                                 LIMIT 1
                                                 ;""", userid)
            firstName = record["first_name"]
            flagLoggedIn = True
        self.render("index.html", flagLoggedIn=flagLoggedIn, firstName=firstName)
        # self.write(":)")
