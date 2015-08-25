import webapp2

from blog.snake import SnakeHandler
from blog.about import AboutHandler
from blog.blog_front import BlogFront
from blog.bubbleshooter import BubbleHandler
from blog.login_logout import Login, Logout
from blog.post import PostPage
from blog.register import Register

app = webapp2.WSGIApplication([('/', BlogFront),
                               ('/?(?:.json)?', BlogFront),
                               ('/([0-9]+)(?:.json)?', PostPage),
                               ('/signup', Register),
                               ('/login', Login),
                               ('/logout', Logout),
                               ('/bubbleshooter', BubbleHandler),
                               ('/snake', SnakeHandler),
                               ('/about', AboutHandler)
                               ],
                              debug=True)