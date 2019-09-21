class TypeError(Exception):

    def __init__(self, message="Incorrect Type"):
        self.message = message

    def getMessage(self):
        return self.message
