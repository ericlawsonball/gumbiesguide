import tornado.web

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

        record = self.application.db.get("""SELECT userid from users
                                            where username=%s and
                                            password=%s limit 1;""",
                                         email, password)
        if record:
            self.set_secure_cookie(record['userid'], expires_days=30)
            self.redirect('/')
        else:
            raise HTTPError(401)
