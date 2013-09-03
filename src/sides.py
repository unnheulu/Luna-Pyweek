from workers import Workers


class PlayerSide:
    def __init__(self, GS):
        self.workers = Workers(GS)
        
        self.resources = {"Rock" : 50,
                          "Metal" : 75,
                          "Crystal" : 5}
    
    def tick(self):
        self.workers.tick()
    
    def blit(self, screen):
        self.workers.blit(screen)