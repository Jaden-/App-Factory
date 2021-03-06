import hmac
import json
import os

import jinja2
import webapp2

from db.Count import Count
from db.User import User

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

# GLOBAL RENDERER #
def render_str(template, **kw):
    t = jinja_env.get_template(template)
    return t.render(kw)

# COOKIE GENERATOR #
secret = "pandabear"

def check_secure_val(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val

def make_secure_val(val):
    return '%s|%s' % (val, hmac.new(secret, val).hexdigest())

# GLOBAL HANDLER #
class GeneralHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **kw):
        kw['user'] = self.user
        kw['registered_users'] = Count.getAllRegisteredUsers()
        kw['comments'] = Count.getAllFrontComments() + Count.getAllSnakeComments()
        t = jinja_env.get_template(template)
        return t.render(kw)

    def get_user(self):
        try:
            return self.user.name
        except:
            return ''

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def render_json(self, d):
        json_txt = json.dumps(d)
        self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'
        self.write(json_txt)

    def set_secure_cookie(self, name, val):
        cookie_val = make_secure_val(val)
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val)
        )

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))

    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))

        if self.request.url.endswith('.json'):
            self.format = 'json'
        else:
            self.format = 'html'