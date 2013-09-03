from mapobjects import ResourceObject, Building
from pathfinder import findPath
from constants import *
import resources as R
import pygame

class Map:
    def __init__(self,GS):
        self.GS = GS
        
        self.offset = [100,0]
        
        self.resources = [ResourceObject("Moonrock", (18,17), (6,4)),ResourceObject("Icefield", (2,5), (4,5))]
        self.buildings = [Building("Base", (15,6), self.GS, preBuilt=True)]
        
        self.createBlockedMap()
        
        self.highlighted = []
    
    def tick(self):
        [i.tick() for i in self.resources]
        [i.tick() for i in self.buildings]
    
    def blit(self,screen):
        screen.blit(R.IMAGES["background"], self.offset)
        [i.blit(screen, self.offset) for i in self.resources]
        [i.blit(screen, self.offset) for i in self.buildings]
        
        if R.DEBUG:
            it = 0
            for i in self.blockedMap:
                jt = 0
                for j in i:
                    if j == 1:
                        pygame.draw.rect(screen,(255,255,255),(jt*20,it*20,20,20),1)
                    if [jt,it] in self.highlighted:
                        pygame.draw.rect(screen,(0,255,255),(jt*20,it*20,20,20),2)
                    jt += 1
                it += 1
    
    
    def newBuilding(self, type, pos, mousePos = False):
        if mousePos:
            pos = [pos[0]-self.offset[0],pos[1]-self.offset[1]]
            pos = [i/20 for i in pos]
        
        building = Building(type, pos, self.GS)
        
        if self.GS.side.resources["Rock"] >= building.toBuild["Rock"] and \
           self.GS.side.resources["Metal"] >= building.toBuild["Metal"]:
            it = 0
            for i in self.blockedMap:
                jt = 0
                for j in i:
                    if j != 0:
                        if pygame.Rect(jt*20,it*20,20,20).colliderect(building.rect):
                            return False
                    jt += 1
                it += 1
            
            canPlace = False
            if R.buildings[type]["place requires"]:
                for i in self.resources:
                    if i.type == R.buildings[type]["place requires"]:
                        if i.rect.colliderect(building.rect):
                            canPlace = True
            if not canPlace:
                return False
            
            self.GS.side.resources["Rock"] -= building.toBuild["Rock"]
            self.GS.side.resources["Metal"] -= building.toBuild["Metal"]
            self.GS.side.resources["Crystal"] -= building.toBuild["Crystal"]
            
            self.buildings.append(building)
            self.GS.side.workers.jobs.append([HIGHPRIORITY,BUILDJOB,building])
            self.createBlockedMap()
            R.cachedPaths = []
            self.GS.side.workers.refindRoutes()
            
            return True
        return False
    
    def createBlockedMap(self):
        self.blockedMap = [[0 for i in range(32)] for i in range(24)]
        
        for i in self.buildings:
            it = 0
            for j in self.blockedMap:
                jt = 0
                for k in j:
                    if pygame.Rect(jt*20,it*20,20,20).colliderect(i.rect):
                        self.blockedMap[it][jt] = 1
                    jt += 1
                it += 1
    
    def findRoute(self,workerPos,targetPos):
        route = findPath(self.blockedMap,workerPos,targetPos)
        self.highlighted = route
        
        return route
    
    def getBase(self):
        for i in self.buildings:
            if i.type == "Base":
                return i
        return False