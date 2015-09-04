from blog.general_handler import GeneralHandler

class TetrisHandler(GeneralHandler):
    def get(self):
        self.render('tetris.html')