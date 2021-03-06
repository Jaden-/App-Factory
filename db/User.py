import hashlib
import random
import string

from google.appengine.ext import db

def make_pw_hash(name, pw, salt = None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)

def valid_pw(name, password, h):
    salt = h.split(',')[0]
    return h == make_pw_hash(name, password, salt)

def make_salt(length = 5):
    return ''.join(random.choice(string.letters) for x in xrange(length))

def users_key(group = 'default'):
    return db.Key.from_path('users', group)

# DB #
class User(db.Model):
    name = db.StringProperty(required=True)
    pw_hash = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    email = db.StringProperty()
    coords = db.GeoPtProperty()

    @classmethod
    def by_id(cls, uid):
        return User.get_by_id(uid, parent = users_key())

    @classmethod
    def by_name(cls, name):
        u = User.all().filter('name =', name).get()
        return u

    @classmethod
    def register(cls, name, pw, email = None, coords=None):
        pw_hash = make_pw_hash(name, pw)
        return User(parent=users_key(),
                    name = name,
                    pw_hash = pw_hash,
                    email = email,
                    coords = coords)

    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name)
        if u and valid_pw(name, pw, u.pw_hash):
            return u