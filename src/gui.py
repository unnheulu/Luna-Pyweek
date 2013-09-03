import resources as R
import pygame

class Menu:
    def __init__(self,rect):
        self.rect = rect
        
        self.contains = {}
    
    def blit(self,screen):
        pygame.draw.rect(screen,(255,255,255),self.rect)
        [self.contains[i].blit(screen) for i in self.contains]
    
    
    def addButton(self,id,button):
        self.contains[id] = button

class Button:
    def __init__(self,rect):
        self.rect = rect
    
    def blit(self,screen):
        pygame.draw.rect(screen,(255,0,0),self.rect)

class GameStateGUI:
    def __init__(self,GS):
        self.GS = GS
        
        self.buildMenu = Menu(pygame.Rect(0,0,100,480))
        self.buildMenu.addButton("Build Ice",Button(pygame.Rect(20,20,60,40)))
        self.buildMenu.addButton("Build Mine",Button(pygame.Rect(20,80,60,40)))
    
    def blit(self,screen):
        self.buildMenu.blit(screen)
        
        screen.blit(R.IMAGES["crystal"],(250,7))
        screen.blit(R.font.render(str(self.GS.side.resources["Crystal"]),1,(0,0,0)),(300,10))
        screen.blit(R.IMAGES["rock"],(350,7))
        screen.blit(R.font.render(str(self.GS.side.resources["Rock"]),1,(0,0,0)),(400,10))
        screen.blit(R.IMAGES["metal"],(450,7))
        screen.blit(R.font.render(str(self.GS.side.resources["Metal"]),1,(0,0,0)),(500,10))