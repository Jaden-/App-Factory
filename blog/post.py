import logging

from google.appengine.ext import db

from blog.general_handler import GeneralHandler
from db.Post import Post

def blog_key(name = 'default'):
    return db.Key.from_path('blog', name)

class PostPage(GeneralHandler):
    def get(self, post_id):
        key = db.Key.from_path('Path', int(post_id), parent=blog_key())
        post = db.get(key)

        if not post:
            self.error(404)
            logging.log(10, '1234567890')
            return
        if self.format == 'html':
            self.render("permalink.html", post = post)
        else:
            self.render_json(post.as_dict())

class NewPost(GeneralHandler):
    def get(self):
        if self.user:
            self.render("newpost.html")
        else:
            self.redirect("/login")

    def post(self):
        if not self.user:
            self.redirect('/')

        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            p = Post(parent = blog_key(), subject = subject, content = content)
            p.put()
            self.redirect('/%s' % str(p.key().id()))
        else:
            error = "subject and content, please!"
            self.render("newpost.html", subject=subject, content=content, error=error)