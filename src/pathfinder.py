import math
import random
import sets
import time
import resources as R

def newNode(newPos, endPos, parent, openList, closedList, rand):
    node = [newPos, parent[1]+1, R.randomNumbers[(rand+parent[1])%1000]+parent[1]+math.sqrt((newPos[0]-endPos[0])**2+(newPos[1]-endPos[1])**2), parent]
    
    for i in closedList:
        if i[0] == node[0]:
            break
    else:
        for i in openList:
            if i[0] == node[0]:
                break
        else:
            openList.append(node)
    
    return openList

def findPath(map, startPos, endPos):
    openList = [[startPos, 0, math.sqrt((startPos[0]-endPos[0])**2+(startPos[1]-endPos[1])**2), None]]
    closedList = []
    currentNode = openList[0]
    
    rand = random.randint(0,1000)
    t = time.time()
    findNextTime = False
    found = False
    while not found:
        newPos = [currentNode[0][0]-1, currentNode[0][1]]
        if newPos[0] >= 0:
            if map[newPos[1]][newPos[0]] == 0:
                openList = newNode(newPos, endPos, currentNode, openList, closedList, rand)
        newPos = [currentNode[0][0]+1, currentNode[0][1]]
        if newPos[0] < len(map[0]):
            if map[newPos[1]][newPos[0]] == 0:
                openList = newNode(newPos, endPos, currentNode, openList, closedList, rand)
        newPos = [currentNode[0][0], currentNode[0][1]-1]
        if newPos[1] >= 0:
            if map[newPos[1]][newPos[0]] == 0:
                openList = newNode(newPos, endPos, currentNode, openList, closedList, rand)
        newPos = [currentNode[0][0], currentNode[0][1]+1]
        if newPos[1] < len(map):
            if map[newPos[1]][newPos[0]] == 0:
                openList = newNode(newPos, endPos, currentNode, openList, closedList, rand)
        
        
        closedList.append(currentNode)
        openList.remove(currentNode)
        
        if not len(openList):
            print time.time()-t
            return []
        
        currentNode = sorted(openList, key=lambda i : i[2])[0]
        
        if currentNode[0] == endPos:
            found = True
        
        #nearest = sorted(openList, key=lambda i : abs(i[0][0]-endPos[0])+abs(i[0][1]-endPos[1]))[0]
        #if abs(nearest[0][0]-endPos[0])+abs(nearest[0][1]-endPos[1]) == 1:
        #    findNextTime = True
            
    node = currentNode
    path = [node]
    while node:
        node = node[3]
        if node:
            path.append(node)
    
    return [i[0] for i in path[::-1]]
    