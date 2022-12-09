from cmu_112_graphics import *
from PIL import Image
from polygonToList import polygonToList
from isInsideTrack import *
from Car import *
from Track import *
from finishLine import *
from findRoute import *
from getSavedRoute import *
from drawPage import *
import numpy as np

import math
import time
FASTCAR = 'IMG/fastCar.png'
SLOWCAR = 'IMG/slowCar.png'
COMPUTERCARSAMPLE = 'IMG/computerCarSample.png'
TRACKSAMPLE = 'Map/trackSample1.jpg'
FINISHLINESAMPLE = 'IMG/finalLine.png'
HISTORYRECORDS = 'Data/historyRecords.txt'


def appStarted(app):

    app.track = Track(TRACKSAMPLE)
    app.finishLine = FinishLine(FINISHLINESAMPLE, x=73, y=123)
    # default is fast car
    app.playerCar = FastCar(FASTCAR, startX=53, startY=123+55)
    app.computerCar = ComputerCar(COMPUTERCARSAMPLE, startX=93, startY=123+55)
    app.startTime = time.time()
    app.raceStartTime = 0
    app.pause = True
    app.page = 1
    app.keyList = set()
    app.timerDelay = 10
    app.isGameStart = False
    app.isGameFinish = False
    app.result = 0
    app.route = []
    app.route.append([app.computerCar.position[0],
                     app.computerCar.position[1], app.computerCar.angle])
    app.isWantToPlayWithAI = False
    app.isAIRouteGenerated = False
    app.isAIWin = False
    app.isPlayerWin = False
    app.AIDifficulty = 1
    app.counter = -1
    app.computerCarWait = 1.8


def restart(app, targetPage=5):
    # default is fast car
    app.playerCar = FastCar(FASTCAR, startX=53, startY=123+55)
    app.computerCar = ComputerCar(COMPUTERCARSAMPLE, startX=93, startY=123+55)
    app.startTime = time.time()
    app.raceStartTime = 0
    app.pause = True
    app.page = targetPage
    app.keyList = set()
    app.timerDelay = 10
    app.isGameStart = False
    app.isGameFinish = False
    app.result = 0
    app.isAIWin = False
    app.isPlayerWin = False
    app.counter = -1
    app.computerCarWait = 1.8


def keyPressed(app, event):
    if (event.key == 'Left'):
        app.keyList.add(event.key)
        # app.playerCar.myRotate(-20)
    elif (event.key == 'Right'):
        app.keyList.add(event.key)
    elif (event.key == 'Up'):
        app.keyList.add(event.key)
    elif (event.key == 'Down'):
        app.keyList.add(event.key)
    elif (event.key == 'p'):
        app.pause = not app.pause
    elif (event.key == 'r'):
        restart(app)


def keyReleased(app, event):
    if (event.key in app.keyList):
        app.keyList.remove(event.key)


def mousePressed(app, event):
    if (app.page == 1):
        if (app.width/2-200 < event.x < app.width/2+200 and 150 < event.y < 250):
            app.page = 2
        elif (app.width/2-200 < event.x < app.width/2+200 and 400 < event.y < 500):
            app.page = 7
    elif (app.page == 2):

        #button: yes
        if (app.width/2-200 < event.x < app.width/2+200 and app.height/3-50 < event.y < app.height/3+50):
            app.page = 3
            app.isWantToPlayWithAI = True
        #button: no
        elif (app.width/2-200 < event.x < app.width/2+200 and app.height/3*2-50 < event.y < app.height/3*2+50):
            # skip to choose map page
            app.page = 4
            app.isWantToPlayWithAI = False

    elif (app.page == 3):
        #button: simple
        if (app.width/2-200 < event.x < app.width/2+200 and app.height/3-50 < event.y < app.height/3+50):
            app.AIDifficulty = 1
        #button: hard
        elif (app.width/2-200 < event.x < app.width/2+200 and app.height/3*2-50 < event.y < app.height/3*2+50):
            app.AIDifficulty = 2
        app.page = 4

    elif (app.page == 4):
        if (app.isWantToPlayWithAI):
            # If the map has cached route
            if (os.path.exists("Data/trackSample1.txt")):
                print('reading saved route')
                app.route = getSavedRoute("Data/trackSample1.txt")
                app.isAIRouteGenerated = True
            else:
                s = time.time()
                print('generating route...')
                findRoute(app)
                print(f'time used:{str(time.time()-s)}')
                app.route = getSavedRoute("Data/trackSample1.txt")
                app.isAIRouteGenerated = True
        app.page = 5
    elif (app.page == 5):

        if (app.width/3-50 < event.x < app.width/3+50 and app.height/2-100 < event.y < app.height/2+100):
            app.playerCar = FastCar(FASTCAR, startX=53, startY=123+55)
        elif (app.width/3*2-50 < event.x < app.width/3*2+50 and app.height/2-100 < event.y < app.height/2+100):
            app.playerCar = SlowCar(SLOWCAR, startX=53, startY=123+55)
        app.page = 6
    elif (app.page == 6 and not app.isGameStart):
        app.raceStartTime = time.time()
        app.pause = False
        app.isGameStart = True

    elif (app.page == 6 and app.isGameStart and not app.isGameFinish):
        if (10 < event.x < 140 and 380 < event.y < 420):
            restart(app, targetPage=2)
        elif (10 < event.x < 140 and 430 < event.y < 470):
            restart(app, targetPage=5)

    elif (app.page == 6 and app.isGameFinish):
        if (app.width/2-100 < event.x < app.width/2+100 and app.height/2+75 < event.y < app.height/2+125):
            restart(app, targetPage=1)

    elif (app.page == 7):
        if (app.width/2-200 < event.x < app.width/2+200 and 450 < event.y < 550):
            app.page = 1


def timerFired(app):

    app.endTime = time.time()

    timePassed = app.endTime-app.startTime

    if (app.isGameStart and not app.pause and not app.isGameFinish):
        if (app.isWantToPlayWithAI):

            # the AI will wait for a while in the beginning to give the user response time
            app.computerCarWait -= timePassed
            if (app.computerCarWait < 0):
                app.counter += app.AIDifficulty
                x, y = app.route[app.counter][0], app.route[app.counter][1]
                if (app.finishLine.isFinish((x, y))):
                    app.isAIWin = True
                    app.isGameFinish = True
                    return
                elif (app.finishLine.isFinish(app.playerCar.position)):
                    app.isPlayerWin = True
                    app.result = str(app.endTime-app.raceStartTime)[:5]

                    with open(HISTORYRECORDS, 'a+') as f:
                        f.write(app.result+'\n')
                    app.isGameFinish = True
                    return

        if (app.finishLine.isFinish(app.playerCar.position)):
            app.result = str(app.endTime-app.raceStartTime)[:5]
            with open(HISTORYRECORDS, 'a+') as f:
                f.write(app.result+'\n')
            app.isGameFinish = True
        else:
            if ('Left' in app.keyList):
                app.playerCar.myRotate(-20, timePassed)
            if ('Right' in app.keyList):
                app.playerCar.myRotate(20, timePassed)
            if ('Down' in app.keyList):
                app.playerCar.brake(timePassed=timePassed)
            if ('Up' in app.keyList):
                app.playerCar.drive(idle=False, timePassed=timePassed)
            if ('Up' not in app.keyList and 'Down' not in app.keyList):
                app.playerCar.drive(idle=True, timePassed=timePassed)
            if (app.playerCar.isCollide(app.track.polygonList)):
                print('collide')
                app.playerCar.velocity = -app.playerCar.velocity

    app.startTime = time.time()


def redrawAll(app, canvas):
    if (app.page == 1):
        drawPage1(app, canvas)
    elif (app.page == 2):
        drawPage2(app, canvas)
    elif (app.page == 3):
        drawPage3(app, canvas)
    elif (app.page == 4):
        drawPage4(app, canvas)
    elif (app.page == 5):
        drawPage5(app, canvas)
    elif (app.page == 6):
        drawPage6(app, canvas)
    elif (app.page == 7):
        drawPage7(app, canvas)


runApp(width=600, height=600)
