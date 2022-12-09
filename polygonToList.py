import cv2
import numpy as np

#I learn opencv from https://www.youtube.com/watch?v=oXlwWbU8l2o
def openCVResize(img,targetSize):
    return cv2.resize(img,(targetSize,targetSize),interpolation=cv2.INTER_AREA)

#*****find contours of a image******
def polygonToList(path,size):
    img=cv2.imread(path,cv2.IMREAD_UNCHANGED)
    #img=openCVResize(img,600)
    imgray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    canny=cv2.Canny(imgray,25,35)
    cnts,hierarchy=cv2.findContours(canny,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    #print(len(cnts))
    #cv2.drawContours(img, cnts,-1,(0, 255, 0), 3)
    #print(list(cnts)[0])
    inner=(cnts[1].tolist())
    outer=(cnts[2].tolist())
    #cv2.imshow('Contours', img)
    #cv2.waitKey()
    
    outerTrack=[]
    innerTrack=[]

    #the result list is a 3d list
    #This function will change it into 1d tuple list.
    for i in range(len(outer)):
        outerTrack.append(tuple(outer[i][0]))
    for i in range(len(inner)):
        innerTrack.append(tuple(inner[i][0]))
    #print(outerTrack,innerTrack)
    return [outerTrack]+[innerTrack]
