from google.appengine.ext.db import GqlQuery, Key

from blog.general_handler import GeneralHandler
from db.Highscore import Highscore

k = Key.from_path('Highscore', 'Content')

class TetrisHandler(GeneralHandler):
    def get(self):
        highscores = GqlQuery("SELECT * FROM Highscore WHERE ANCESTOR IS :1 ORDER BY highscore DESC", k)
        self.render('tetris.html', highscores=highscores)

    def post(self):
        name = self.get_user()
        highscore = self.request.get('highscore_get')
        if not name:
            self.render('tetris.html', error="You are not logged in.")
        else:
            h = Highscore(name=name, highscore=float(highscore), parent=k)
            h.put()
            self.redirect('/tetris')