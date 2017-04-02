import tornado.web
import random

class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        userid = self.get_secure_cookie('userid')
        # if self.current_user:
        if userid:
            name = tornado.escape.xhtml_escape(self.get_secure_cookie('userid'))
            self.render('login.html', msg = 'Already logged in as ' + name)
        else:
            self.render('login.html', msg = '')

    def post(self):
        email = self.get_argument('email')
        password = self.get_argument('password')

        record = self.application.db.get("""SELECT userid
                                             FROM users
                                             WHERE username=%s
                                             AND password=%s
                                             LIMIT 1
                                             ;""", email, password)
        if record:
            self.set_secure_cookie('userid', record['userid'], expires_days=30)
            self.redirect('/')
        else:
            self.render('login.html', msg = 'Bad email/password! (Attempt ID: '
                                             + str(random.randint(1000,9999))
                                             + ')')
