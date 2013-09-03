from controllers import Controller
from map import Map
from gui import GameStateGUI
from sides import PlayerSide
from constants import *
import resources as R
import pygame

class GameState:
    def __init__(self):
        self.controller = Controller(self)
        
        self.side = PlayerSide(self)
        self.map = Map(self)
        self.gui = GameStateGUI(self)
    
    def handleEvents(self,events):
        self.controller.handleEvents(events)
    
    def tick(self):
        self.map.tick()
        self.side.tick()
    
    def blit(self,screen):
        screen.fill((0,0,0))
        self.map.blit(screen)
        self.side.blit(screen)
        
        self.gui.blit(screen)
        
        if self.controller.action[0] == PLACEOBJECT:
            screen.blit(R.IMAGES[R.buildings[self.controller.action[1]]["image"]],([i/20*20 for i in pygame.mouse.get_pos()]))