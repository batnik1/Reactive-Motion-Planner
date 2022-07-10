# Agent Class
class Agent:
    def __init__(self,pos):
        # choose a random start point
        self.pos=pos
        self.path=[]
        self.velocity=[0,0]
        self.max_speed=1
        self.max_force=0.1
        self.mass=1
        self.radius=1
        self.goal=(0,0)
        self.I=0
        self.early=pos
        self.trajectory=[]
        self.lastseen=pos
        self.me=0