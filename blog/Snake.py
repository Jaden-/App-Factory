from google.appengine.ext.db import GqlQuery
from blog.general_handler import GeneralHandler
from db.SnakeComment import SnakeComment


class SnakeHandler(GeneralHandler):
    def get(self):
        comments = GqlQuery("SELECT * FROM SnakeComment ORDER BY created DESC LIMIT 4")

        self.render('snake.html', snakeComments=comments);

    def post(self):
        author = self.get_user()
        content = self.request.get('snakeContent')

        if content:
            c = SnakeComment(snakeContent=content, author=author)
            c.put()
            self.redirect('/snake')
        else:
            error = "You have to write a comment to submit"
            self.render('snake.html', error)