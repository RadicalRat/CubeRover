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


        self.angle  = 0 #change obvi
        self.speed = abs(rX)*100
        

    def vel_calc(self, trig):
        #10 cm/s fastest speed. wheel radius 7.5 inches. 
        #1 inch is 2.54 cm
        #need rotations per minute, rpm * 2pi / 60 = w
        #v=wr
        #trig vals are 0-2
        radme = 7.5 * 2.54/100
        angspeed = .1/radme
        maxrpm = angspeed * 60/(2*np.pi)
        maxencoder = maxrpm*28
        return trig/2 * maxencoder


        #return trig/2 * 100
    

rX = 1
rY = 0
calc = ValConverter()
calc.angle_calc(1, 0)
print(calc.speed, calc.angle)



