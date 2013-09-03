import pygame
import resources as R
import random

class MapObject:
    def tick(self):
        pass
    
    def blit(self, screen, offset):
        screen.blit(self.image, [self.rect.left+offset[0], self.rect.top+offset[1]])


class ResourceObject(MapObject):
    def __init__(self, type, pos, size):
        self.type = type
        self.rect = pygame.Rect((pos[0]*20,pos[1]*20),(size[0]*20,size[1]*20))
        
        self.image = pygame.Surface(self.rect.size)
        self.image.fill(R.resourceObjects[self.type]["colour"])


class Building(MapObject):
    def __init__(self, type, pos, GS, preBuilt=False):
        self.type = type
        size = R.buildings[self.type]["size"]
        self.image = R.buildings[self.type]["image"]
        self.rect = pygame.Rect((pos[0]*20,pos[1]*20),(size[0]*20,size[1]*20))
        
        self.toBuild = None
        
        if not preBuilt:
            self.toBuild = R.buildings[self.type]["costs"]
            self.image += "_build"
            
            self.pending = self.toBuild.copy()
            
            self.totalNeeded = self.toBuild["Rock"]+self.toBuild["Metal"]+self.toBuild["Crystal"]
            self.totalLeft = self.totalNeeded
        
        self.produces = R.buildings[self.type]["produces"]
        self.produceTimers = {}
        if self.produces:
            for i in self.produces:
                self.produceTimers[i] = random.randint(self.produces[i][0],self.produces[i][1])
        
        self.contains = {"Rock" : 0,
                         "Metal" : 0,
                         "Crystal" : 0}
    
    def blit(self, screen, offset):
        screen.blit(R.IMAGES[self.image], [self.rect.left+offset[0], self.rect.top+offset[1]])
        
        if self.toBuild:
            pygame.draw.rect(screen,(0,128,0),(self.rect.left+offset[0],self.rect.top+offset[1]-10,self.rect.width,5))
            if self.totalNeeded-self.totalLeft:
                pygame.draw.rect(screen,(0,255,0),(self.rect.left+offset[0],self.rect.top+offset[1]-10,self.rect.width*(self.totalNeeded-self.totalLeft)/float(self.totalNeeded),5))
    
    def tick(self):
        if self.toBuild:
            if self.totalLeft == 0:
                self.toBuild = None
                self.image = R.buildings[self.type]["image"]
        
        for i in self.produceTimers:
            self.produceTimers[i] -= 1
            if self.produceTimers[i] <= 0:
                self.contains[i] += 1
                self.produceTimers[i] = random.randint(self.produces[i][0],self.produces[i][1])