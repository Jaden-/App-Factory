import logging

from google.appengine.ext.db import GqlQuery

from blog.general_handler import GeneralHandler
from db.User import User

GMAPS_URL = "https://maps.googleapis.com/maps/api/staticmap?size=800x400&sensor=false&"

def gmaps_img(points):
    markers = '&'.join('markers=%s,%s' % (p.lat, p.lon) for p in points)
    return GMAPS_URL + markers

class GoogleMapsHandler(GeneralHandler):
    def get(self):
        users = GqlQuery("SELECT * FROM User")

        users = list(users)
        logging.log(40, "Users: " + repr(users))

        points = filter(None, (u.coords for u in users))
        logging.log(40, "Points: " + repr(points))

        img_url = None
        if points:
            img_url = gmaps_img(points)

        self.render('google-maps.html', img_url=img_url, users=users)

    def post(self):
        pass