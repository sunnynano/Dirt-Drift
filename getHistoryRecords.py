def getHistoryRecords(path):
    f = open(path)
    lines = f.read()
    result = []
    for line in lines.splitlines():
        result.append(float(line))
    result.sort()
    f.close()
    return (result[:7])
