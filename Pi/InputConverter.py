import numpy as np



def turn_calc(rX, rY, trig):
    rX = .01 if rX == 0 else rX

    wheel_radius = 15 #cm
    encoder = 5281.7 #en/rot

    fraction = rY/rX
    angle = np.arctan(fraction) * 180/np.pi

    #linear speed
    ang = linvel_calc(trig)

    #turning radius
    min = .2048 
    max = 1.60 #based off of bailey's mobility tests

    range = max-min

    radius = abs(rY) * range + min #normalizes 

    ang = anglin_calc(trig)

    if rX > 0:
        norm_angle = 90-angle
        r1 = radius+.2048
        r2 = radius-.2048

    else:
        norm_angle = -90-angle
        r1 = radius-20.48
        r2 = radius+20.48


    vel1 = ang*r1/(2*np.pi) #rot/sec
    vel2 = ang*r2/(2*np.pi)
    
    vel1_enc = vel1*encoder
    vel2_enc = vel2*encoder

    return norm_angle, radius, abs(vel1_enc), abs(vel2_enc)

def anglin_calc(trig):
    max_speed = 35 #cm/s
    wheel_radius = 15 #cm

    max_ang = (max_speed/wheel_radius)
    ang = trig/2 * max_ang
    return ang

def linvel_calc(trig):
    #10 cm/s fastest speed. wheel radius 15 cm 
    #1 inch is 2.54 cm
    #need rotations per minute, rpm * 2pi / 60 = w
    #v=wr
    #trig vals are 0-2
    encoder = 5281.7 #enc/rot
    max_speed = 35 #cm/s
    wheel_radius = 15 #cm

    max_enc = (max_speed/wheel_radius)/(2*np.pi)*encoder #max val in en/s

    enc_speed = trig/2 * max_enc

    return enc_speed

def testvel_calc(vel):
    encoder = 5281.7 #enc/rot
    wheel_radius = 15 #cm

    if vel > 35:
        vel = 35

    enc_speed = (vel/wheel_radius)/(2*np.pi)*encoder #max val in en/s

    return enc_speed




    #return trig/2 * 100

# rX= 0
# rY = -1
# angle, x, y, vel1, vel2 =  turn_calc(rX, rY)
# print(vel1, vel2)
# rX = 1
# rY = 0
# calc = ValConverter()
# calc.angle_calc(1, 0)
# print(calc.speed, calc.angle)




