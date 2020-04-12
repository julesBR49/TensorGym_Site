import copy

def displayPartialList(pList):
    strx = ""
    newList = copy.deepcopy(pList)
    while len(newList) > 0:
        part = newList[0]
        if part.isSquare():
            i = 0
            found = False
            while i < len(newList):
                checkPart = newList[i]
                if checkPart.getIndex().sumsWith(part.getIndex()):
                # if part2.getIndex().basicEquals(checkPart.getIndex()):
                    strx += "\\square "
                    newList.pop(i)
                    newList.remove(part)
                    found = True
                    i = len(newList)
                i += 1
            if not found:
                strx += repr(part)
                newList.remove(part)
        else:
            strx += repr(part)
            newList.remove(part)

    return strx