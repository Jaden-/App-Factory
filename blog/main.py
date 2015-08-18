import webapp2
from blog.FredrikSnake import FredrikSnakeHandler
from blog.IvarSnake import IvarSnakeHandler

from blog.blog_front import BlogFront
from blog.bubbleshooter import BubbleHandler

from blog.login_logout import Login, Logout
from blog.post import PostPage
from blog.post import NewPost
from blog.register import Register

app = webapp2.WSGIApplication([('/', BlogFront),
                               ('/?(?:.json)?', BlogFront),
                               ('/([0-9]+)(?:.json)?', PostPage),
                               ('/newpost', NewPost),
                               ('/signup', Register),
                               ('/login', Login),
                               ('/logout', Logout),
                               ('/bubbleshooter', BubbleHandler),
                               ('/snake_fredrik', FredrikSnakeHandler),
                               ('/snake_ivar', IvarSnakeHandler)
                               ],
                              debug=True)