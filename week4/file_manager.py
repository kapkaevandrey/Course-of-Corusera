import os.path
import tempfile
import uuid


class File():
    def __init__(self, path):
        self.position = 0
        self.path = path
        if not os.path.exists(self.path):
            open(self.path, "w").close()

    def read(self):
        with open(self.path, "r") as f:
            return f.read()

    def write(self, data):
        with open(self.path, "w") as f:
            f.write(data)
        return len(data)

    def __str__(self):
        return os.path.join(tempfile.gettempdir(), self.path)

    def __iter__(self):
        return self

    def __next__(self):
        with open(self.path) as f:
            f.seek(self.position)
            line = f.readline()
            if not line:
                self.position = 0
                raise StopIteration
            self.position = f.tell()

            return line

    def __add__(self, other):
        new_path = os.path.join(os.path.dirname(self.path), str(uuid.uuid4().hex))
        new_file = File(new_path)
        new_file.write(self.read() + other.read())
        return new_file


