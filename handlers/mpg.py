import tornado.web
from datetime import datetime

class MpgHandler(tornado.web.RequestHandler):
    def post(self):
        miles = float(self.get_argument('miles'))
        gallons = float(self.get_argument('gallons'))
        dollars = float(self.get_argument('dollars'))
        self.application.db.query("""INSERT INTO mpg (miles, gallons, dollars,
                                      mileage, cost_per_mile, timestamp)
                                      VALUES (%s, %s, %s, %s, %s, %s)""",
                                      miles, gallons, dollars,
                                      miles / gallons, dollars / miles, str(datetime.now())
                                      )
        # self.render('mpg-results.html', miles=miles, gallons=gallons, dollars=dollars)
        records = self.application.db.query("""SELECT *
                                               FROM mpg
                                               ORDER BY timestamp DESC
                                               LIMIT 30
                                               """)
        self.render('mpg-results.html', records=records)

    def get(self):
        self.render('mpg-calc.html')

class MpgViewHandler(tornado.web.RequestHandler):
    def get(self):
        records = self.application.db.query("""SELECT *
                                               FROM mpg
                                               ORDER BY timestamp DESC
                                               LIMIT 30
                                               """)
        self.render('mpg-results.html', records=records)
