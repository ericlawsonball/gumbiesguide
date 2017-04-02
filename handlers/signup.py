import tornado.web

class SignupHandler(tornado.web.RequestHandler):
    def get(self):
        # userid = self.get_secure_cookie('userid')
        if self.current_user:
        # if userid:
            self.redirect('/')
        else:
            self.render("signup.html")

    def post(self):
        email = self.get_argument('email')
        if '@' not in email:
             raise tornado.web.HTTPError(401)
        password1 = self.get_argument('password1')
        password2 = self.get_arugment('password2')

        if password1 == password2:
            self.write("Thank you for signing up!  Please confirm:" + email
                        + "    Password = " + password)
        else:
            self.write("Your passwords do not match!")
