import logging

from google.appengine.ext.db import GqlQuery

from blog.general_handler import GeneralHandler
from db.FrontComment import FrontComment

INFO_LEVEL = 20
ERROR_LEVEL = 40


class BlogFront(GeneralHandler):
    def get(self):
        logged_out = self.request.get('logged_out')
        logged_in = self.request.get('logged_in')
        registered = self.request.get('registered')
        all_comments = self.request.get('allComments')

        if all_comments == 'True':
            logging.log(ERROR_LEVEL, 'showing all comments')
            comments = GqlQuery("SELECT * FROM FrontComment ORDER BY created DESC")

        else:
            logging.log(ERROR_LEVEL, 'showing recent comments')
            comments = GqlQuery("SELECT * FROM FrontComment ORDER BY created DESC LIMIT 4")


        if self.format == 'html':
            self.render('front.html', frontComments=comments, logged_in=logged_in, logged_out=logged_out,
                        registered=registered)
        else:
            return self.render_json([p.as_dict() for p in comments])

    def post(self):
        author = self.get_user()
        content = self.request.get('frontContent')

        if content:
            c = FrontComment(frontContent=content, author=author)
            c.put()
            self.redirect('/')
        else:
            error = "Please submit some content!"
            self.render("front.html", content=content, error=error)