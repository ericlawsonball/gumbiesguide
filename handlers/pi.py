import tornado.web

class PiHandler(tornado.web.RequestHandler):
    def get(self):
        pi = str(math.pi)
        piLong = '3. ' + textwrap.fill("""141592653589793238462643
                                          383279502884197169399375
                                          105820974944592307816406
                                          286208998628034825342117
                                          067982148086513282306647
                                          093844609550582231725359
                                          408128481117450284102701
                                          938521105559644622948954
                                          93038196""",6)
        self.render("pi.html", piPython = pi, piLong = piLong)
