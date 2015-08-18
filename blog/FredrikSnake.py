from blog.general_handler import GeneralHandler


class FredrikSnakeHandler(GeneralHandler):
    def get(self):
        self.render('fredrik-snake.html');