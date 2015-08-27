from google.appengine.ext import db

g_front_comments = 0
g_snake_comments = 0
g_users = 0

class Count(db.Model):
    @staticmethod
    def setAllSnakeComments(comments):
        global g_snake_comments
        g_snake_comments = comments

    @staticmethod
    def setAllFrontComments(comments):
        global g_front_comments
        g_front_comments = comments

    @staticmethod
    def setAllRegisteredUsers(users):
        global g_users
        g_users = users

    @staticmethod
    def getAllFrontComments():
        return g_front_comments

    @staticmethod
    def getAllSnakeComments():
        return g_snake_comments

    @staticmethod
    def getAllRegisteredUsers():
        return g_users