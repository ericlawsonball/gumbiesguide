import tornado.web
import datetime
import uuid

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
        password1 = self.get_argument('password1')
        password2 = self.get_argument('password2')

        if password1 == password2:
            password = password1

            record = self.application.db.query(
            """SELECT username FROM users
            WHERE username = %s
            LIMIT 1""",
            email
            )

            if record:
                self.write("You already have an account for " + email)
            else:
                self.application.db.query(
                    """INSERT INTO users (
                    userid, username, password, first_name, status, date_created)
                    VALUES (%s, %s, %s, %s, %s, %s)""",
                    str(uuid.uuid4()), email, password,
                    'NewUser', 'Active', datetime.datetime.today()
                    )
                self.write("Thank you for signing up!  Please confirm:" + email
                            + "    Password = " + password)
        else:
            self.write("Your passwords do not match!")
