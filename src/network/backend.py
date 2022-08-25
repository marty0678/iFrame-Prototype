import json
from PySide6.QtCore import QObject, Slot


class Backend(QObject):
    def __init__(self):
        super().__init__()
        self.input = None

    @Slot(str, result=str)
    def set(self, input):
        self.input = json.loads(input)
        print(f"Client sent {self.input}")

    @Slot(result=str)
    def get(self):
        print(f"Client received {self.input}")
        return json.dumps(self.input)
