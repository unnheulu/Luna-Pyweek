from constants import *
import resources as R
import pygame
import threading
import random

class Worker:
    def __init__(self,GS,pos):
        self.GS = GS
        
        self.rect = pygame.Rect(pos,(20,20))
        #self.image = pygame.Surface((20,20),65536)
        #pygame.draw.ellipse(self.image,(255,192,0),(0,0,20,20))
        self.image = R.IMAGES["astronaut"]
        
        self.selected = False
        self.targetRoute = []
        
        self.job = [NOJOB]
        self.carrying = NOCARRY
    
    def tick(self):
        self.move()
        self.doJob()
    
    def blit(self,screen, offset):
        screen.blit(self.image,(self.rect.left+offset[0],self.rect.top+offset[1]-20))
        if self.selected:
            pygame.draw.rect(screen,(255,0,0),(self.rect.left+offset[0],self.rect.top+offset[1]-20,20,40),1)
    
    
    def doJob(self):
        if self.job[0] == BUILDJOB:
            if self.job[1].toBuild == None:
                self.job = [NOJOB]
                return
            
            if not self.targetRoute:
                basePos = [i/20 for i in self.GS.map.getBase().rect.topleft]
                buildingPos = [i/20 for i in self.job[1].rect.topleft]
                workerPos = [i/20 for i in self.rect.topleft]
                
                if self._byBuilding(workerPos,basePos,[5,5]) and self.carrying == NOCARRY:
                    if self.job[1].pending["Rock"] > 0:
                        self.job[1].pending["Rock"] -= 1
                        self.carrying = ROCKCARRY
                    elif self.job[1].pending["Metal"] > 0:
                        self.job[1].pending["Metal"] -= 1
                        self.carrying = METALCARRY
                    elif self.job[1].pending["Crystal"] > 0:
                        self.job[1].pending["Crystal"] -= 1
                        self.carrying = CRYSTALCARRY
                    
                    self.findPathToBuilding(self.job[1],buildingPos)
                
                elif self._byBuilding(workerPos,buildingPos,[i/20 for i in self.job[1].rect.size]) and self.carrying:
                    if self.carrying == ROCKCARRY:
                        self.job[1].toBuild["Rock"] -= 1
                    if self.carrying == METALCARRY:
                        self.job[1].toBuild["Metal"] -= 1
                    if self.carrying == CRYSTALCARRY:
                        self.job[1].toBuild["Crystal"] -= 1
                    
                    self.job[1].totalLeft -= 1
                    
                    self.carrying = NOCARRY
                
                elif self.carrying == NOCARRY:
                    self.findPathToBuilding(self.GS.map.getBase(),basePos)
                
                elif self.carrying:
                    self.findPathToBuilding(self.job[1],buildingPos)
    
    def move(self):
        if len(self.targetRoute):
            if self.rect.left < self.targetRoute[0][0]*20:
                self.rect.left += 1
            if self.rect.left > self.targetRoute[0][0]*20:
                self.rect.left -= 1
            if self.rect.top < self.targetRoute[0][1]*20:
                self.rect.top += 1
            if self.rect.top > self.targetRoute[0][1]*20:
                self.rect.top -= 1
            
            if self.rect.topleft == (self.targetRoute[0][0]*20,self.targetRoute[0][1]*20):
                self.targetRoute.pop(0)
    
    
    def _boxBuilding(self,building):
        """Returns a box of squares around a building"""
        
        widthInSquares = building.rect.width/20
        heightInSquares = building.rect.height/20
        
        box = []
        
        for i in range(-1,widthInSquares+1):
            for j in range(-1,heightInSquares+1):
                if j in range(0,heightInSquares) and i in [-1,widthInSquares] or \
                   i in range(0,widthInSquares) and j in [-1,heightInSquares]:
                    box.append([i,j])
        
        return box
    
    def _byBuilding(self,workerPos,buildingPos,buildingSize):
        if workerPos[0] in range(buildingPos[0]-1,buildingPos[0]+buildingSize[0]+1):
            if workerPos[1] in range(buildingPos[1]-1,buildingPos[1]+buildingSize[1]+1):
                return True
        return False
    
    def findPathToBuilding(self,building,endPos):
        workerPos = [i/20 for i in self.rect.topleft]
        
        routes = []
        for i in self._boxBuilding(building):
            skip = False
            
            if self.GS.map.blockedMap[endPos[1]+i[1]][endPos[0]+i[0]] != 0:
                continue
            
            for j in R.badPaths:
                if j[0] == workerPos and j[1] == [endPos[0]+i[0],endPos[1]+i[1]]:
                    skip = True
            
            """
            for j in R.cachedPaths:
                if len(j):
                    if j[0] == workerPos and j[-1] == [endPos[0]+i[0],endPos[1]+i[1]]:
                        routes.append(j)
                        skip = True"""
            
            if skip == False:
                route = self.GS.map.findRoute(workerPos, [endPos[0]+i[0],endPos[1]+i[1]])
                if route:
                    R.cachedPaths.append(route)
                    routes.append(route)
                else:
                    R.badPaths.append([workerPos,[endPos[0]+i[0],endPos[1]+i[1]]])
        
        routes = sorted(routes, key=lambda i : len(i))
        if routes:
            self.targetRoute = routes[random.randint(0,min(len(routes)-1,2))]