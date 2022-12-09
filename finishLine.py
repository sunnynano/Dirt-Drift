from cmu_112_graphics import *
from PIL import Image


class FinishLine(object):
    def __init__(self, path, x, y):
        self.img = Image.open(path)
        self.readyToDraw = ImageTk.PhotoImage(self.img)
        self.x = x
        self.y = y

    def isFinish(self, position):
        if (self.y+5 > position[1] > self.y-5 and self.x-50 < position[0] < self.x+50):
            return True
        return False
