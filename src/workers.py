from worker import Worker
from constants import *
import time

class Workers:
    def __init__(self, GS):
        self.GS = GS
        
        self.workers = [Worker(self.GS,[260,160]),Worker(self.GS,[260,180]),Worker(self.GS,[240,180]),Worker(self.GS,[240,160]),
                        Worker(self.GS,[260,160]),Worker(self.GS,[260,180]),Worker(self.GS,[240,180]),Worker(self.GS,[240,160])]
        
        self.jobs  = []
    
    def tick(self):
        for i in self.workers:
            i.tick()
            if i.job[0] == NOJOB:
                newJob = self.getJob()
                if len(newJob) > 0:
                    i.job = newJob[0][1::]
    
    def blit(self, screen):
        [i.blit(screen, self.GS.map.offset) for i in self.workers]
    
    def moveWorker(self, worker, pos):
        workerPos = [i/20 for i in worker.rect.topleft]
        
        worker.targetRoute = self.GS.map.findRoute(workerPos,pos)
    
    def refindRoutes(self):
        for i in self.workers:
            workerPos = [j/20 for j in i.rect.topleft]
            if len(i.targetRoute):
                #if self.GS.map.blockedMap[i.targetRoute[-1][1]][i.targetRoute[-1][0]] == 1:
                i.targetRoute = []
    
    def getWorker(self, pos):
        for i in self.workers:
            i.rect.top -= 20
            i.rect.height = 40
            if i.rect.collidepoint(pos):
                i.rect.top += 20
                i.height = 20
                return i
            i.rect.top += 20
            i.rect.height = 20
    
    def getJob(self):
        for i in self.jobs:
            if i[1] == BUILDJOB:
                if i[2].toBuild == None:
                    self.jobs.remove(i)
        return sorted(self.jobs, key=lambda i : i[0])