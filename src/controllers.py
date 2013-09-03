import pygame
import sys

from constants import *

class Controller:
    def __init__(self,GS):
        self.GS = GS
        
        self.action = [NOACTION]
    
    def handleEvents(self,events):
        for i in events:
            if i.type == pygame.QUIT:
                sys.exit()
            if i.type == pygame.KEYDOWN:
                if i.key == pygame.K_ESCAPE:
                    sys.exit()
            if i.type == pygame.MOUSEBUTTONDOWN:
                if i.button == 1:
                    worker = self.GS.side.workers.getWorker(i.pos)
                    if self.GS.gui.buildMenu.contains["Build Ice"].rect.collidepoint(i.pos):
                        self.action = [PLACEOBJECT, "Ice Purifier"]
                        pygame.mouse.set_visible(False)
                    if self.GS.gui.buildMenu.contains["Build Mine"].rect.collidepoint(i.pos):
                        self.action = [PLACEOBJECT, "Mining Station"]
                        pygame.mouse.set_visible(False)
                    
                    elif self.action[0] == PLACEOBJECT:
                        if self.GS.map.newBuilding(self.action[1], i.pos, mousePos = True):
                            self.cleanUp()
                    
                    elif self.action[0] == SELECTWORKER:
                        self.GS.side.workers.moveWorker(self.action[1], [j/20 for j in i.pos])
                    
                    elif worker:
                        self.cleanUp()
                        self.action = [SELECTWORKER, worker]
                        worker.selected = True
                    
                if i.button == 3:
                    self.cleanUp()
                    
                    #else:
                    #    self.GS.side.workers.moveWorker(i.pos)
            
        if pygame.mouse.get_pos()[0] < 20:
            self.GS.map.offset[0] += 2
        if pygame.mouse.get_pos()[0] > 620:
            self.GS.map.offset[0] -= 2
        if pygame.mouse.get_pos()[1] < 20:
            self.GS.map.offset[1] += 2
        if pygame.mouse.get_pos()[1] > 460:
            self.GS.map.offset[1] -= 2
                
    
    def cleanUp(self):
        if self.action[0] == SELECTWORKER:
            self.action[1].selected = False
        self.action = [NOACTION]
        pygame.mouse.set_visible(True)