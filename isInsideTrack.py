

'''
def isValidIntersect(x,y,start,end,possibleIntersection):
    if((start[1]<y and end[1]<y) or 
       (start[1]>y and end[1]>y) or
       (start[1]==end[1]) or
       (start[1]==y and end[1]>y) or 
       (end[1]==y and start[1]>y) or
       (start[0]<x and end[1]<y)):
        return False

    kInverse=(end[0]-start[0])/(end[1]-start[1])  #no division-by-zero problem
    intersection=-y*kInverse+end[1]*kInverse+end[0]
    possibleIntersection.append([intersection,start,end])
    if intersection<=x: 
        return False
    return True

#count the intersections of the ray(staring at x,y and extending to the right) and the polygon
#if there are odd intersections, then the point is inside the polygon 
def isInside(x,y,polygonList):
    count=0
    possilbleIntersection=[]
    for i in range(len(polygonList)):
        for j in range(len(polygonList[i])-1):
            start=polygonList[i][j]
            end=polygonList[i][j+1]
            if(isValidIntersect(x,y,start,end,possilbleIntersection)):
                count+=1
    #print(possilbleIntersection)
    return [count%2==1,possilbleIntersection]
'''

def isValidIntersect(x,y,start,end):
    if((start[1]<y and end[1]<y) or 
       (start[1]>y and end[1]>y) or
       (start[1]==end[1]) or
       (start[1]==y and end[1]>y) or 
       (end[1]==y and start[1]>y) or
       (start[0]<x and end[1]<y)):
        return False

    kInverse=(end[0]-start[0])/(end[1]-start[1])  #no division-by-zero problem
    intersection=-y*kInverse+end[1]*kInverse+end[0]
    if intersection<=x: 
        return False
    return True

#count the intersections of the ray(staring at x,y and extending to the right) and the polygon
#if there are odd intersections, then the point is inside the polygon 
def isInside(x,y,polygonList):
    count=0
    for i in range(len(polygonList)):
        for j in range(len(polygonList[i])-1):
            start=polygonList[i][j]
            end=polygonList[i][j+1]
            if(isValidIntersect(x,y,start,end)):
                count+=1
    return count%2==1
