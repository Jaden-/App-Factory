from google.appengine.ext.db import GqlQuery
from blog.general_handler import GeneralHandler
from db.Count import Count


class BubbleHandler(GeneralHandler):
    def get(self):
        count = Count(google_clicks=0, snake_clicks=0, bubble_clicks=1)
        count.put()
        self.render('bubbleshooter.html')