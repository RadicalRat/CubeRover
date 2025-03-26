import numpy as np

class ValConverter:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.angle = 0
        self.speed = 0

    def angle_calc(self, rX, rY):
        # self.angle = np.arctan2(rY, rX) #radians from [-pi to pi]
        # squared = rY**2 + rX**2
        # self.speed = np.sqrt(squared)/np.sqrt(2) * .1 #max output is sqrt(2), so on a scale from 0-.1 m/s
        frac = rY/rX
        self.angle = np.degrees(np.arctan(frac))
        mag = np.sqrt(rY**2 + rX**2)
        if abs(self.angle) == 0:
            self.speed = 100
        elif abs(self.angle) == 90:
            self.speed == 0
        else:
            self.speed = abs(rX)*100
        

    def vel_calc(self, trig):
        #10 cm/s fastest speed. wheel radius 6 inches. 
        #1 inch is 2.54 cm
        #need rotations per minute, rpm * 2pi / 60 = w
        #v=wr
        #trig vals are 0-2
        return trig/2 * 100
    

rX = 1
rY = 0
calc = ValConverter()
calc.angle_calc(1, 0)
print(calc.speed, calc.angle)



