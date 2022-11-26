import threading

from Options import Options


class Embed(threading.Thread):

    def __init__(self, file, mode):
        super(Embed, self).__init__()
        self.daemon = True

        Options.load_settings(self)

        # Save attributes
        self.file = file
        self.filename = self.file.split("/")[-1]
        self.mode = mode

    def run(self):
        print("embedder run")
