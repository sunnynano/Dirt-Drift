def getSavedRoute(path):
    f=open(path)
    lines=f.read()
    result=[]
    for line in lines.splitlines():
        result.append([])
        lst=line.split(' ')
        for i in range(3):
            result[-1].append(eval(lst[i]))
        #print(eval(lst[0]))
    f.close()
    return(result)

