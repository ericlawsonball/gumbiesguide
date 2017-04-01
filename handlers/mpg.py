import tornado.web
from datetime import datetime

class MpgHandler(tornado.web.RequestHandler):
    def post(self):
        miles = float(self.get_argument('miles'))
        gallons = float(self.get_argument('gallons'))
        dollars = float(self.get_argument('dollars'))
        self.application.db.query("""INSERT INTO mpg (miles, gallons, dollars,
                                      mileage, cost_per_mile, date)
                                      VALUES (%s, %s, %s, %s, %s, %s)""",
                                      miles, gallons, dollars,
                                      miles / gallons, dollars / miles, str(datetime.now())
                                      )
        # self.render('mpg-results.html', miles=miles, gallons=gallons, dollars=dollars)
        records = self.application.db.query("SELECT * FROM mpg LIMIT 30")
        x = 10
        self.render('mpg-results.html', m=miles, g=gallons, d=dollars,
                    records=records, x=x)

    def get(self):
        self.render('mpg-calc.html')
