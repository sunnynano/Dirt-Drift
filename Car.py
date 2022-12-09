from cmu_112_graphics import *
from PIL import Image
from polygonToList import polygonToList
from isInsideTrack import *
import numpy as np

import math
import time

#normalize a vector from https://stackoverflow.com/questions/21030391/how-to-normalize-a-numpy-array-to-a-unit-vector
def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0: 
       return v
    return v / norm

def vectorRotate(v,dAngle):
    newX=v[0]*np.cos(dAngle)+v[1]*np.sin(dAngle)
    newY=-v[0]*np.sin(dAngle)+v[1]*np.cos(dAngle)
    return np.array([newX,newY])

#calculate the angle between v and (0,1)
def getAngle(v):
    if(1-10**-5<v[1]<1+10**-5):
        v[1]=1
    cos=math.degrees(np.arccos(v[1]))
    sin=math.degrees(np.arcsin(v[0]))
    if(cos>=0 and sin>=0):
        return math.radians(cos-360)
    elif(cos>=0 and sin<=0):
        return math.radians(-cos)

def createVector(angle,length=1):
    return np.array([np.sin(np.deg2rad(angle)),np.cos(np.deg2rad(angle))])*length

def vectorAngle(v1,v2):
    return(np.rad2deg(np.arccos((v1.dot(v2))/(np.linalg.norm(v1)*np.linalg.norm(v2)))))



#I learned car physics from https://asawicki.info/Mirror/Car%20Physics%20for%20Games/Car%20Physics%20for%20Games.html and
#https://www.youtube.com/watch?v=mJ1ZfGDTMCY and http://engineeringdotnet.blogspot.com/2010/04/simple-2d-car-physics-in-games.html

class AbstractCar(object):
    def __init__(self,path,startX,startY):
        self.img=Image.open(path)
        self.img=self.img.resize((20,40),Image.ANTIALIAS)
        self.readyToDraw=ImageTk.PhotoImage(self.img)
        self.angle=0

        self.mass=1500
        self.brakeConstant=9000
        self.dragConstant=8.257
        self.rollingConstant=228
        #             reverse, 1,  2,   3,  4, 5, 6
        self.gearRatio=[2.90,2.66,1.78,1.3,1,0.74,0.5]
        self.differentialRatio=3.42
        self.wheelRadius=0.34
        self.wheelDistance=50

        self.direction=np.array([0,1])
        self.rpm=1000
        self.lowestRpm=1000
        self.highestRpm=6000
        self.currentGear=1
        self.accelaration=np.array([0,0])
        self.velocity=np.array([0,0])
        self.position=np.array([startX,startY])
        
        self.engineTorque=self.getTorque(self.rpm)
        self.tractionForce=self.direction*self.engineTorque*self.gearRatio[self.currentGear]*self.differentialRatio*0.7/self.wheelRadius
        self.dragForce=-self.dragConstant*self.velocity*np.linalg.norm(self.velocity)
        self.rollingResistance=-self.rollingConstant*self.velocity
        self.long=self.tractionForce+self.dragForce+self.rollingResistance

    def getTorque(self,rpm):
        return 465.9252*math.e**(-(rpm - 3609.714)**2/(2*4480.701**2))

    def drive(self,idle=True,timePassed=0.01):
        
        #under idle condition (not pressing throttle but engine has started), a car still has engine torque
        if(idle):
            self.engineTorque=self.getTorque(self.lowestRpm)/5
        else:
            self.engineTorque=self.getTorque(self.rpm)
        self.tractionForce=self.direction*self.engineTorque*self.gearRatio[self.currentGear]*self.differentialRatio*0.7/self.wheelRadius
        self.dragForce=-self.dragConstant*self.velocity*np.linalg.norm(self.velocity)
        self.rollingResistance=-self.rollingConstant*self.velocity
        self.long=self.tractionForce+self.dragForce+self.rollingResistance
        self.updateAcceVeloPosi(timePassed)

    def brake(self,timePassed=0.01):
        self.braking=-self.direction*self.brakeConstant
        self.dragForce=-self.dragConstant*self.velocity*np.linalg.norm(self.velocity)
        self.rollingResistance=-self.rollingConstant*self.velocity
        self.long=self.braking+self.dragForce+self.rollingResistance
        self.updateAcceVeloPosi(timePassed)

    def updateAcceVeloPosi(self,timePassed):
        self.accelaration=self.long/self.mass
        self.velocity=self.velocity+timePassed*self.accelaration
        self.position=self.position+timePassed*self.velocity
        tempRpm=np.linalg.norm(self.velocity)/self.wheelRadius*self.gearRatio[self.currentGear]*self.differentialRatio*30/math.pi
        if(tempRpm>self.highestRpm):
            self.rpm=self.highestRpm
        elif(tempRpm<self.lowestRpm):
            self.rpm=self.lowestRpm
        else:
            self.rpm=tempRpm
    

    def myRotate(self,inputAngle,timePassed):
        radius=self.wheelDistance/math.sin(math.radians(inputAngle))
        angleVelocity=np.linalg.norm(self.velocity)/radius
        dAngle=angleVelocity*5
        if(dAngle!=0):
            frontWheel=self.position-self.wheelDistance/2*self.direction+self.velocity*timePassed*5
            rotatedVelocity=vectorRotate(self.velocity,-dAngle)
            rareWheel=self.position+self.wheelDistance/2*self.direction+rotatedVelocity*timePassed*5
            self.direction=normalize(rareWheel-frontWheel)
            angle=vectorAngle(self.velocity,self.direction)

            #reverse
            if(angle<0 or angle>=90):
                self.velocity=-self.direction*np.linalg.norm(self.velocity)
            #forward
            else:
                self.velocity=self.direction*np.linalg.norm(self.velocity)
            self.angle=math.degrees(getAngle(self.direction))
            #print(self.angle)

            self.readyToDraw=ImageTk.PhotoImage(self.img.rotate(self.angle,resample=Image.BICUBIC, expand=True))
    '''
        self.angle=(self.angle+math.degrees(dAngle))%360
        ang=math.radians(self.angle)
        self.direction=np.array([-np.sin(ang),-np.cos(ang)])
        #self.accelaration=self.direction*np.linalg.norm(self.accelaration)
        #self.velocity= self.direction*np.linalg.norm(self.velocity)
    '''
        
    def isCollide(self,polygonList):
        absoluteCoordianteOffsetX=self.position[0]
        absoluteCoordianteOffsetY=self.position[1]
        distance=math.sqrt(10**2+20**2)

        #check four corners
        for ang in [(-120-self.angle),(-240-self.angle),(-60-self.angle),(60-self.angle)]:
            ang=math.radians(ang)
            x0=distance*math.cos(ang)+absoluteCoordianteOffsetX
            y0=distance*math.sin(ang)+absoluteCoordianteOffsetY
            if(not isInside(x0,y0,polygonList)):
                #print(x0,y0)
                return True
        return False


class PlayerCar(AbstractCar):
    pass

class FastCar(PlayerCar):
    def getTorque(self,rpm):
        return 3065.9252*math.e**(-(rpm - 3609.714)**2/(2*4480.701**2))

class SlowCar(PlayerCar):
    def getTorque(self,rpm):
        return 665.9252*math.e**(-(rpm - 3609.714)**2/(2*4480.701**2))

class TestCar(AbstractCar):
    def getTorque(self,rpm):
        return 1465.9252*math.e**(-(rpm - 3609.714)**2/(2*4480.701**2))

class ComputerCar(AbstractCar):

    def myRotate(self,inputAngle,timePassed):
        self.angle=(self.angle+inputAngle)%360
        self.direction=vectorRotate(np.array([0,1]),math.radians(self.angle))
        self.accelaration=self.direction*np.linalg.norm(self.accelaration)
        self.velocity=self.direction*np.linalg.norm(self.velocity)
        self.readyToDraw=ImageTk.PhotoImage(self.img.rotate(self.angle,resample=Image.BICUBIC, expand=True))



