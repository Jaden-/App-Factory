from blog.general_handler import GeneralHandler


class AboutHandler(GeneralHandler):
    def get(self):
        self.render("about.html")