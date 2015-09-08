import webapp2

from blog.google_maps import GoogleMapsHandler
from blog.live_chat import LiveChatHandler
from blog.Snake import SnakeHandler
from blog.about import AboutHandler
from blog.blog_front import BlogFront
from blog.bubbleshooter import BubbleHandler
from blog.login_logout import Login, Logout
from blog.post import PostPage
from blog.register import Register
from blog.tetris import TetrisHandler

app = webapp2.WSGIApplication([('/', BlogFront),
                               ('/?(?:.json)?', BlogFront),
                               ('/([0-9]+)(?:.json)?', PostPage),
                               ('/signup', Register),
                               ('/login', Login),
                               ('/logout', Logout),
                               ('/googlemaps', GoogleMapsHandler),
                               ('/bubbleshooter', BubbleHandler),
                               ('/snake', SnakeHandler),
                               ('/livechat', LiveChatHandler),
                               ('/about', AboutHandler),
                               ('/tetris', TetrisHandler)
                               ],
                              debug=True)