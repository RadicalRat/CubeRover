import numpy as np

class AngleConverter:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.angle = 0
        self.pwm = 0

    def calc(self, rX, rY):
        self.angle = np.arctan2(rY, rX) #radians from [-pi to pi]
        squared = rY**2 + rX**2
        self.pwm = np.sqrt(squared) *255 #max output should be one, so on a scale from 0-255
