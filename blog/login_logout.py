import logging
from blog.general_handler import GeneralHandler
from db import User


class Login(GeneralHandler):
    def get(self):
        self.render('login-form.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        logging.log(10, 'Login: 1234567890')

        u = User.User.login(username, password)
        if u:
            self.login(u)
            self.redirect('/?logged_in=True')
        else:
            msg = 'Invalid login'
            self.render('login-form.html', error = msg)

class Logout(GeneralHandler):
    def get(self):
        self.logout()
        self.redirect('/?logged_out=True')

class Welcome(GeneralHandler):
    def get(self):
        if self.user:
            self.redirect('/')
        else:
            self.redirect('/signup')