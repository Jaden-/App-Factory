import logging

from google.appengine.ext.db import GqlQuery, Key

from blog.general_handler import GeneralHandler
from db.Highscore import Highscore

k = Key.from_path('Highscore', 'Content')

class TetrisHandler(GeneralHandler):
    def get(self):
        highscores = GqlQuery("SELECT * FROM Highscore WHERE ANCESTOR IS :1 ORDER BY highscore DESC", k)
        self.render('tetris.html', highscores=highscores)

    def post(self):
        name_html = self.get_user()
        logging.log(40, 'User: ' + name_html)
        highscore_html = self.request.get('highscore_get')
        if not name_html:
            self.render('tetris.html', error="You are not logged in.")
        else:
            logging.log(40, "IN ELSE")
            try_highscore = Highscore(name=name_html, highscore=float(highscore_html), parent=k)
            all_highscores = GqlQuery("SELECT * FROM Highscore WHERE ANCESTOR IS :1", k)

            count = 0

            for highscore in all_highscores:
                if highscore.name == name_html:
                    count += 1
                    logging.log(40, "NAME EQUALS NAME")
                    if try_highscore.highscore > highscore.highscore:
                        logging.log(40, "FOUND HIGHER SCORE")
                        highscore.delete()
                        try_highscore.put()
                    else:
                        logging.log(40, "try_highscore: " + str(try_highscore.highscore) + ' is not higher than ' +
                                    ' highscore.highscore: ' + str(highscore.highscore))
                else:
                    logging.log(40, "Name: " + highscore.name + ' is not equal to: ' + name_html)

            if count == 0:
                try_highscore.put()

        self.redirect('/tetris')
