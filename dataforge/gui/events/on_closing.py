import sys


def on_closing(self):
    self.root.destroy()
    sys.exit()
