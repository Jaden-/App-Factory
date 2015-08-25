from google.appengine.ext import db

# Comments under the game Snake #
from blog.general_handler import render_str


class SnakeComment(db.Model):
    snakeContent = db.TextProperty(required=False)
    author = db.TextProperty(required=False)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)

    def render(self):
        self._render_text = self.snakeContent #replace('\n', '<br>')
        self._author_ = self.author
        return render_str("post.html", p=self)

    def as_dict(self):
        time_fmt = '%c'
        d = {'content': self.snakeContent,
             'author': self.author,
             'created': self.created.strftime(time_fmt),
             'last_modified': self.last_modified.strftime(time_fmt)}
        return d
