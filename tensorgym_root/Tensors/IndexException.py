class IndexException(Exception):

    def __init__(self, message="Incorrect index instances"):
        self.message = message

    def getMessage(self):
        return self.message
