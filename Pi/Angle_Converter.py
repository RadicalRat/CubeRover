import numpy as np

class AngleConverter:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.angle = 0

    def calc(rX, rY):
        return np.atan(rY/rX)