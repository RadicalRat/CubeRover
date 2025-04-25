import numpy as np



def turn_calc(rX, rY):
    rX = .01 if rX == 0 else rX

    fraction = rY/rX
    angle = np.arctan(fraction) * 180/np.pi

    squared = rY**2 + rX**2
    speed = np.sqrt(squared)/np.sqrt(2) * .1 #max output is sqrt(2), so on a scale from 0-.1 m/s

    #turning radius
    min = 0 
    max = 160 #based off of bailey's mobility tests

    range = max-min

    radius = abs(rY)/180 * range + min #normalizes ry val to max of 1

    ang = speed/(2*np.pi)

    if rX > 0:
        norm_angle = 90-angle
        r1 = radius-20.48
        r2 = radius+20.48

    else:
        norm_angle = -90-angle
        r1 = radius+20.48
        r2 = radius-20.48


    vel1 = ang*r1
    vel2 = ang*r2

    return norm_angle, radius, speed, vel1, vel2

def linvel_calc(trig):
    #10 cm/s fastest speed. wheel radius 7.5 inches. 
    #1 inch is 2.54 cm
    #need rotations per minute, rpm * 2pi / 60 = w
    #v=wr
    #trig vals are 0-2
    radme = 7.5 * 2.54/100
    angspeed = .1/radme
    maxrpm = angspeed * 60/(2*np.pi)
    maxencoder = maxrpm*537.7
    return trig/2 * maxencoder



    #return trig/2 * 100


# rX = 1
# rY = 0
# calc = ValConverter()
# calc.angle_calc(1, 0)
# print(calc.speed, calc.angle)




