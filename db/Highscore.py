from google.appengine.ext import db

class Highscore(db.Model):
    name = db.TextProperty(required=True)
    highscore = db.FloatProperty(required=True)