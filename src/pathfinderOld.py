import math
import random

class Node:
    def __init__(self, pos, endPos, parent=None):
        self.pos = pos
        self.parent = parent
        
        if self.parent:
            self.distance = parent.distance+1
        else:
            self.distance = 0
        
        #self.heuristic = random.randint(0,4) + self.distance + math.sqrt((self.pos[0]-endPos[0])**2+
        #                                                                 (self.pos[1]-endPos[1])**2)
        self.heuristic = self.distance + abs(self.pos[0]-endPos[0])+abs(self.pos[1]-endPos[1])

def newNode(node, openList, closedList):
    for i in closedList:
        if i.pos == node.pos:
            break
    else:
        for i in openList:
            if i.pos == node.pos:
                break
        else:
            openList.append(node)
    
    return openList

def findPath(map, startPos, endPos):
    openList = [Node(startPos,endPos)]
    closedList = []
    currentNode = openList[0]
    
    found = False
    while not found:
        newPos = [currentNode.pos[0]-1, currentNode.pos[1]]
        if newPos[0] >= 0:
            if map[newPos[1]][newPos[0]] == 0:
                openList = newNode(Node(newPos, endPos, currentNode), openList, closedList)
        newPos = [currentNode.pos[0]+1, currentNode.pos[1]]
        if newPos[0] < len(map[0]):
            if map[newPos[1]][newPos[0]] == 0:
                openList = newNode(Node(newPos, endPos, currentNode), openList, closedList)
        newPos = [currentNode.pos[0], currentNode.pos[1]-1]
        if newPos[1] >= 0:
            if map[newPos[1]][newPos[0]] == 0:
                openList = newNode(Node(newPos, endPos, currentNode), openList, closedList)
        newPos = [currentNode.pos[0], currentNode.pos[1]+1]
        if newPos[1] < len(map):
            if map[newPos[1]][newPos[0]] == 0:
                openList = newNode(Node(newPos, endPos, currentNode), openList, closedList)
        
        
        closedList.append(currentNode)
        openList.remove(currentNode)
        
        if not len(openList):
            return []
        
        openList = sorted(openList, key=lambda i : i.heuristic)
        currentNode = openList[0]
        
        if currentNode.pos == endPos:
            found = True
            
    node = currentNode
    path = [node]
    while node:
        node = node.parent
        if node:
            path.append(node)
    
    return [i.pos for i in path[::-1]]
    