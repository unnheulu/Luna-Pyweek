import pygame
import random
import os

pygame.init()

IMAGES = {}
for i in os.listdir(os.path.join("..","art")):
    IMAGES[i[:-4]] = pygame.image.load(os.path.join("..","art",i))

resourceObjects = {"Icefield" : {"colour" : (160,176,224)},
                   "Moonrock" : {"colour" : (144,128,192)}}

buildings = {"Base" : {"size" : [3,3],
                       "image" : "base",
                       "colour" : (224,224,255),
                       "produces" : None},
             "Ice Purifier" : {"size" : [2,2],
                               "image" : "icepure",
                               "colour" : (224,224,255),
                               "place requires" : "Icefield",
                               "produces" : None,
                               "costs" : {"Rock" : 10,
                                          "Metal" : 20,
                                          "Crystal" : 0}},
             "Mining Station" : {"size" : [2,3],
                               "image" : "minestation",
                               "colour" : (224,224,255),
                               "produces" : {"Rock" : (20,50),
                                             "Metal" : (50,150),
                                             "Crystal" : (300,750)},
                               "place requires" : "Moonrock",
                               "costs" : {"Rock" : 10,
                                          "Metal" : 15,
                                          "Crystal" : 1}}}

cachedPaths = []
badPaths = []

font = pygame.font.SysFont("Free Sans", 24)
textFont = pygame.font.SysFont("Courier", 12)
textFontHead = pygame.font.SysFont("Courier", 13, 1)

DEBUG = False

randomNumbers = [random.randint(0,40) for i in range(1000)] #Used for pathfinding 'cause it's kinda slow to do it afterwards
#sparedNodes = [[Node()]]