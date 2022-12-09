import copy
import math
import numpy as np
def findRoute(app,timePassed=0.7):

    if(app.finishLine.isFinish(app.computerCar.position)):
        if(not app.isAIRouteGenerated):
            print('finish!')   
            app.isAIRouteGenerated=True
            app.route=makeRouteSmoother(app.route)
            app.route=makeRouteSmoother(app.route)
            app.route=makeRouteSmoother(app.route)
            #print(app.route)
            np.savetxt("Data/trackSample1.txt",app.route)
            return True
    else:
        previousState=copy.copy(app.computerCar)
        for angle in [0,2.5,-2.5]:
            if(angle==0):
                app.computerCar.drive(idle=False,timePassed=timePassed)
            else:
                
                app.computerCar.myRotate(angle,timePassed=timePassed)
                app.computerCar.drive(idle=True,timePassed=timePassed)
            if(not app.computerCar.isCollide(app.track.polygonList)):
                print(app.computerCar.position)
                app.route.append([app.computerCar.position[0],app.computerCar.position[1],app.computerCar.angle])
                if(findRoute(app)):
                    return True
                app.route.pop()
            app.computerCar=previousState
        return False

def makeRouteSmoother(route):
    newRoute=[]
    for i in range(len(route)-1):
        
        curr=copy.copy(route[i])
        newRoute.append(curr)
        following=copy.copy(route[i+1])
        distance=math.sqrt((curr[0]-following[0])**2+(curr[1]-following[1])**2)
        if(distance>1):
            x=(curr[0]+following[0])/2
            y=(curr[1]+following[1])/2
            angle=(curr[2]+following[2])/2
            newRoute.append([x,y,angle])
    newRoute.append(route[-1])
    return newRoute
