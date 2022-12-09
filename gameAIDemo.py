from cmu_112_graphics import *
from PIL import Image
from polygonToList import polygonToList
from isInsideTrack import *
from getSavedRoute import *
import numpy as np
from Car import *
import math
import time
import copy
import os
CARSAMPLE = 'IMG/fastCar.png'
TRACKSAMPLE = 'Map/trackSample1.jpg'
FINISHLINESAMPLE = 'IMG/finalLine.png'


# In the future, there will be different kinds of track
class AbstractTrack(object):
    def __init__(self, path, friction=0.1):
        self.img = Image.open(path)
        self.img = self.img.resize((600, 600), Image.ANTIALIAS)
        self.readyToDraw = ImageTk.PhotoImage(self.img)
        self.friction = friction
        self.polygonList = polygonToList(path, size=600)


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


def appStarted(app):
    app.computerCar = ComputerCar(CARSAMPLE, startX=93, startY=123+55)
    app.track = AbstractTrack(TRACKSAMPLE)
    app.finishLine = FinishLine(FINISHLINESAMPLE, x=73, y=123)
    app.startTime = time.time()
    app.pause = False
    app.page = 1
    app.past = []
    app.keyList = set()
    app.timerDelay = 10
    app.route = []

    app.route.append([app.computerCar.position[0],
                     app.computerCar.position[1], app.computerCar.angle])
    app.isFinish = False
    app.counter = -1


def mousePressed(app, event):
    s = time.time()
    if (os.path.exists("Data/trackSample1.txt")):
        print('reading saved route')
        app.route = getSavedRoute("Data/trackSample1.txt")
        app.isFinish = True
    else:
        print('generating route')
        findRoute(app)
        print(f'time used:{str(time.time()-s)}')
    if (app.page == 1):
        if (app.width/2-200 < event.x < app.width/2+200 and 150 < event.y < 250):
            app.page += 1
    elif (app.page == 2):
        app.page += 1
    elif (app.page == 3):
        app.page += 1


def findRoute(app, timePassed=0.7):

    if (app.finishLine.isFinish(app.computerCar.position)):
        if (not app.isFinish):
            print('finish!')
            app.isFinish = True
            app.route = makeRouteSmoother(app.route)
            app.route = makeRouteSmoother(app.route)
            app.route = makeRouteSmoother(app.route)
            app.route = makeRouteSmoother(app.route)
            app.route = makeRouteSmoother(app.route)
            app.route = makeRouteSmoother(app.route)

            print(app.route)
            np.savetxt("Data/trackSample1.txt", app.route)
            return True
    else:
        previousState = copy.copy(app.computerCar)
        for angle in [0, 2.5, -2.5]:
            if (angle == 0):
                app.computerCar.drive(idle=False, timePassed=timePassed)
            else:

                app.computerCar.myRotate(angle, timePassed=timePassed)
                app.computerCar.drive(idle=True, timePassed=timePassed)
            if (not app.computerCar.isCollide(app.track.polygonList)):
                print(app.computerCar.position)
                app.route.append(
                    [app.computerCar.position[0], app.computerCar.position[1], app.computerCar.angle])
                if (findRoute(app)):
                    return True
                app.route.pop()
            app.computerCar = previousState
        return False


def makeRouteSmoother(route):
    newRoute = []
    for i in range(len(route)-1):

        curr = copy.copy(route[i])
        newRoute.append(curr)
        following = copy.copy(route[i+1])
        distance = math.sqrt((curr[0]-following[0])
                             ** 2+(curr[1]-following[1])**2)
        if (distance > 1):
            x = (curr[0]+following[0])/2
            y = (curr[1]+following[1])/2
            angle = (curr[2]+following[2])/2
            newRoute.append([x, y, angle])
    newRoute.append(route[-1])
    return newRoute


def timerFired(app):
    if (app.isFinish):
        app.counter += 6

# state:[x,y,angle]


def drawComputerCar(counter, canvas, state):
    x, y, angle = state[counter][0], state[counter][1], state[counter][2]
    currentImage = Image.open(CARSAMPLE)
    currentImage = currentImage.resize((20, 40), Image.ANTIALIAS)
    currentImage = ImageTk.PhotoImage(currentImage.rotate(
        angle, resample=Image.BICUBIC, expand=True))
    canvas.create_image(x, y, image=currentImage)


def drawPage4(app, canvas):
    canvas.create_image(app.width/2, app.height/2, image=app.track.readyToDraw)
    canvas.create_image(app.finishLine.x, app.finishLine.y,
                        image=app.finishLine.readyToDraw)
    if (app.isFinish):
        for i in range(len(app.route)):
            canvas.create_oval(
                app.route[i][0]-1, app.route[i][1]-1, app.route[i][0]+1, app.route[i][1]+1)
        if (app.counter < len(app.route)):
            drawComputerCar(app.counter, canvas, app.route)


def redrawAll(app, canvas):
    drawPage4(app, canvas)


runApp(width=600, height=600)
