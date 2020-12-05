class FileReader:
    def __init__(self, path):
        self.path = path

    def read(self):
       try:
        with open(self.path, "r") as file:
            return file.read()
       except FileNotFoundError:
           return ""

