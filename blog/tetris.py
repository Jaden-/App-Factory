import hashlib
import logging
from google.appengine.ext.db import GqlQuery, Key

from blog.general_handler import GeneralHandler
from db.Highscore import Highscore

k = Key.from_path('Highscore', 'Content')

secret = 'jdks'

class TetrisHandler(GeneralHandler):
    def get(self):
        highscores = GqlQuery("SELECT * FROM Highscore WHERE ANCESTOR IS :1 ORDER BY highscore DESC", k)
        self.render('tetris.html', highscores=highscores)

    def post(self):
        name_html = self.get_user()
        score_html = self.request.get('highscore_get')
        speed_html = self.request.get('speed_get')
        multiplier_html = self.request.get('multiplier_get')
        hash_client = self.request.get('hash_get')

        hash_server = hashlib.sha256(str(score_html) + str(speed_html) + str(multiplier_html) + secret).hexdigest()

        if not name_html:
            self.render('tetris.html', error="You are not logged in.")
        elif hash_server != hash_client:
            self.render('tetris.html', error="Screw you Espen! Now you can't cheat your way up!")
        else:
            try_highscore = Highscore(name=name_html, highscore=float(score_html), speed=float(speed_html),
                                      multiplier=float(multiplier_html), parent=k)
            all_highscores = GqlQuery("SELECT * FROM Highscore WHERE ANCESTOR IS :1", k)

            count = 0
            for highscore in all_highscores:
                if highscore.name == name_html:
                    count += 1
                    if try_highscore.highscore > highscore.highscore:
                        highscore.delete()
                        try_highscore.put()

            if count == 0:
                try_highscore.put()

            self.redirect('/tetris')