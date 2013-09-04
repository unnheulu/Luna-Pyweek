import resources as R
import pygame

class Menu:
    def __init__(self,rect,image):
        self.rect = rect
        self.image = image
        
        self.images = []
        self.contains = {}
    
    def blit(self,screen):
        #pygame.draw.rect(screen,(255,255,255),self.rect)
        screen.blit(self.image,self.rect)
        [self.contains[i].blit(screen) for i in self.contains]
        for i in self.images:
            screen.blit(i[1],i[0])
    
    def addImage(self,pos,image):
        self.images.append([pos,image])
    
    def addButton(self,id,button):
        self.contains[id] = button

class Button:
    def __init__(self,rect,image):
        self.rect = rect
        self.image = image
    
    def blit(self,screen):
        screen.blit(self.image,self.rect)

class GameStateGUI:
    def __init__(self,GS):
        self.GS = GS
        
        self.buildMenu = Menu(pygame.Rect(0,0,100,480),R.IMAGES["buildMenu"])
        self.buildMenu.addImage((20,20), R.textFontHead.render("Build", 1, (0,0,0)))
        self.buildMenu.addButton("Build Ice",Button(pygame.Rect(20,50,90,12),R.textFont.render("Ice Extractor",1,(0,0,0))))
        self.buildMenu.addButton("Build Mine",Button(pygame.Rect(20,70,90,12),R.textFont.render("Mine",1,(0,0,0))))
    
    def blit(self,screen):
        self.buildMenu.blit(screen)
        
        screen.blit(R.IMAGES["crystal"],(250,7))
        screen.blit(R.font.render(str(self.GS.side.resources["Crystal"]),1,(0,0,0)),(300,10))
        screen.blit(R.IMAGES["rock"],(350,7))
        screen.blit(R.font.render(str(self.GS.side.resources["Rock"]),1,(0,0,0)),(400,10))
        screen.blit(R.IMAGES["metal"],(450,7))
        screen.blit(R.font.render(str(self.GS.side.resources["Metal"]),1,(0,0,0)),(500,10))