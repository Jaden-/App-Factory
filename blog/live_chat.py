from blog.general_handler import GeneralHandler


class LiveChatHandler(GeneralHandler):
    def get(self):
        self.render('live-chat.html')

    def post(self):
        pass