from gamestate import GameState
from constants import *
import pygame

class Main:
    def __init__(self):
        self.states = {GAMESTATE : GameState()}
        self.currentState = GAMESTATE
    
    def checkEvents(self):
        pygame.event.pump()
        events = pygame.event.get()
        
        self.states[self.currentState].handleEvents(events)
    
    def tick(self):
        self.states[self.currentState].tick()
    
    def blit(self,screen):
        self.states[self.currentState].blit(screen)
        pygame.display.flip()
    
    def run(self):
        screen = pygame.display.set_mode((640,480))
        
        clock = pygame.time.Clock()
        while True:
            clock.tick(30)
            
            self.checkEvents()
            self.tick()
            self.blit(screen)

M = Main()
M.run()