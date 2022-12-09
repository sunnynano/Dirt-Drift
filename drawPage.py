from cmu_112_graphics import *
from PIL import Image
from Car import *
from getHistoryRecords import *
import numpy as np
FASTCAR='IMG/fastCar.png'
SLOWCAR='IMG/slowCar.png'
COMPUTERCARSAMPLE='IMG/computerCarSample.png'
TRACKSAMPLE='Map/trackSample1.jpg'
FINISHLINESAMPLE='IMG/finalLine.png'
HISTORYRECORDS='Data/historyRecords.txt'
#start page
def drawPage1(app,canvas):
    canvas.create_text(app.width/2,50,text='112 Racing',font='Helvetica 35',anchor='n')
    canvas.create_text(app.width/2,200,text='START',font='Helvetica 25')
    canvas.create_rectangle(app.width/2-200,150,app.width/2+200,250)
    canvas.create_text(app.width/2,450,text='History Records',font='Helvetica 25')
    canvas.create_rectangle(app.width/2-200,400,app.width/2+200,500)

#choose to play with AI
def drawPage2(app,canvas):
    canvas.create_text(app.width/2,app.height/6,text='Do you want play with a game AI?',font='Helvetica 25')
    canvas.create_text(app.width/2,app.height/3,text='yes',font='Helvetica 25')
    canvas.create_rectangle(app.width/2-200,app.height/3-50,app.width/2+200,app.height/3+50)    
    canvas.create_text(app.width/2,app.height/3*2,text='no',font='Helvetica 25')  
    canvas.create_rectangle(app.width/2-200,app.height/3*2-50,app.width/2+200,app.height/3*2+50)  

#choose AI difficulty
def drawPage3(app,canvas):
    canvas.create_text(app.width/2,app.height/6,text='Choose AI difficulty',font='Helvetica 25')
    canvas.create_text(app.width/2,app.height/3,text='Simple',font='Helvetica 25')
    canvas.create_rectangle(app.width/2-200,app.height/3-50,app.width/2+200,app.height/3+50)    
    canvas.create_text(app.width/2,app.height/3*2,text='Hard',font='Helvetica 25')  
    canvas.create_rectangle(app.width/2-200,app.height/3*2-50,app.width/2+200,app.height/3*2+50)  

#choose map
def drawPage4(app,canvas):
    canvas.create_text(app.width/2,app.height/10,text='Choose your map',font='Helvetica 25')
    trackDisplay1=ImageTk.PhotoImage(Image.open(TRACKSAMPLE).resize((200,200),Image.ANTIALIAS))
    canvas.create_image(app.width/2,app.height/2,image=trackDisplay1)

#choose car
def drawPage5(app,canvas):
    canvas.create_text(app.width/2,app.height/10,text='Choose your car',font='Helvetica 25',anchor='n')
    carDisplay1=ImageTk.PhotoImage(Image.open(FASTCAR).resize((100,200),Image.ANTIALIAS))
    carDisplay2=ImageTk.PhotoImage(Image.open(SLOWCAR).resize((100,200),Image.ANTIALIAS))
    canvas.create_image(app.width/3,app.height/2,image=carDisplay1)
    canvas.create_text(app.width/3,app.height/6*5,text='Fast car',font='Helvetica 15')
    canvas.create_image(app.width/3*2,app.height/2,image=carDisplay2)
    canvas.create_text(app.width/3*2,app.height/6*5,text='Slow car',font='Helvetica 15')


def drawComputerCar(counter,canvas,state):
    if(counter<=0): counter=0
    x,y,angle=state[counter][0],state[counter][1],state[counter][2]
    currentImage=Image.open(COMPUTERCARSAMPLE)
    currentImage=currentImage.resize((20,40),Image.ANTIALIAS)
    currentImage=ImageTk.PhotoImage(currentImage.rotate(angle,resample=Image.BICUBIC, expand=True))
    canvas.create_image(x,y,image=currentImage)

def drawPage6(app,canvas):
    canvas.create_image(app.width/2,app.height/2,image=app.track.readyToDraw)    
    if(not app.isGameStart):
        canvas.create_text(app.width/2,app.height/2,text='Press anywhere on the screen to start the game',font='Helvetica 15')
    else:
        canvas.create_image(app.finishLine.x,app.finishLine.y,image=app.finishLine.readyToDraw)
        if(app.isAIRouteGenerated and app.isWantToPlayWithAI):
            if(app.counter<len(app.route)):
                drawComputerCar(app.counter,canvas,app.route)
        canvas.create_image(app.playerCar.position[0],app.playerCar.position[1],image=app.playerCar.readyToDraw)

        #display player car info
        canvas.create_text(20,500,text=f'v:{str(np.linalg.norm(app.playerCar.velocity))[:3]}',anchor='w')
        canvas.create_text(20,530,text=f'a:{str(np.linalg.norm(app.playerCar.accelaration))[:3]}',anchor='w')
        canvas.create_text(20,550,text=f'rpm:{app.playerCar.rpm}',anchor='w')

        '''
        for i in range(len(app.past)):
            canvas.create_oval(app.past[i][0]-1,app.past[i][1]-1,app.past[i][0]+1,app.past[i][1]+1)
        '''
    if(app.isGameFinish):
        if(app.isWantToPlayWithAI):
            if(app.isAIWin):
                canvas.create_text(app.width/2,app.height/2-50,text=f'You lose!',font='Helvetica 25')
            elif(app.isPlayerWin):
                canvas.create_text(app.width/2,app.height/2-50,text=f'You win!',font='Helvetica 25')
                canvas.create_text(app.width/2,app.height/2,text=f'Your result is: {app.result}s',font='Helvetica 25')    
        else:
            canvas.create_text(app.width/2,app.height/2-50,text=f'Your result is: {app.result}s',font='Helvetica 25')
        
        canvas.create_text(app.width/2,app.height/2+100,text='play again',font='Helvetica 25')
        canvas.create_rectangle(app.width/2-100,app.height/2+75,app.width/2+100,app.height/2+125,outline='black')
    if(app.isGameStart and not app.isGameFinish):
        canvas.create_text(20,400,text='change AI settings',anchor='w')
        canvas.create_rectangle(10,380,140,420)
        canvas.create_text(20,450,text='change car settings',anchor='w')
        canvas.create_rectangle(10,430,140,470)    


def drawPage7(app,canvas):
    result=getHistoryRecords(HISTORYRECORDS)
    canvas.create_text(app.width/2,70,text='History Records',font='Helvetica 25')
    for i in range(len(result)):
        canvas.create_text(app.width/2-60,120+i*50,text=f'{i+1}.  {result[i]}',font='Helvetica 20',anchor='w')
    canvas.create_text(app.width/2,500,text='Back to home page',font='Helvetica 25')
    canvas.create_rectangle(app.width/2-200,450,app.width/2+200,550)