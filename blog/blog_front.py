from blog.general_handler import GeneralHandler
from db import Post

class BlogFront(GeneralHandler):
    def get(self):
        logged_out = self.request.get('logged_out')
        logged_in = self.request.get('logged_in')
        registered = self.request.get('registered')
        posts = Post.Post.all().order('-created')
        if self.format == 'html':
            self.render('front.html', posts=posts, logged_in=logged_in, logged_out=logged_out,
                        registered=registered)
        else:
            return self.render_json([p.as_dict() for p in posts])