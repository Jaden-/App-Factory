import logging
from google.appengine.ext.db import GqlQuery
from blog.general_handler import GeneralHandler
from db.Highscore import Highscore


class TetrisHandler(GeneralHandler):
    def get(self):
        highscores = GqlQuery("SELECT * FROM Highscore ORDER BY highscore DESC")
        self.render('tetris.html', highscores=highscores)

    def post(self):
        name = self.get_user()
        highscore = self.request.get('highscore_get')
        h = Highscore(name=name, highscore=highscore)
        h.put()
        highscores = GqlQuery("SELECT * FROM Highscore ORDER BY highscore DESC")
        self.render('tetris.html', highscores=highscores)
