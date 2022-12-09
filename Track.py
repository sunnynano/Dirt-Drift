
from cmu_112_graphics import *
from PIL import Image
from polygonToList import polygonToList
class Track(object):
    def __init__(self,path):
        self.img=Image.open(path)
        self.img=self.img.resize((600,600),Image.ANTIALIAS)
        self.readyToDraw=ImageTk.PhotoImage(self.img)
        self.polygonList=polygonToList(path,size=600)
