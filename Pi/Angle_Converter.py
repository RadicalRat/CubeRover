import numpy as np

class AngleConverter:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.angle = 0
        self.speed = 0

    def calc(self, rX, rY):
        self.angle = np.arctan2(rY, rX) #radians from [-pi to pi]
        squared = rY**2 + rX**2
        self.speed = np.sqrt(squared)/np.sqrt(2) * .1 #max output is sqrt(2), so on a scale from 0-.1 m/s
