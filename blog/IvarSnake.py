from blog.general_handler import GeneralHandler


class IvarSnakeHandler(GeneralHandler):
    def get(self):
        self.render('ivar-snake.html')
