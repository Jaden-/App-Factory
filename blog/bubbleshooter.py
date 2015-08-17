from blog.general_handler import GeneralHandler

class BubbleHandler(GeneralHandler):
    def get(self):
        self.render('bubbleshooter.html')