import struct
import time
import serial
import traceback
import pySerialTransfer as pySer

import Network.Networking as network
from Angle_Converter import AngleConverter

serveraddress = ('0.0.0.0', 5555)
server = network.NetworkHost(serveraddress)
server.listenaccept()


# arduinoCom = serialSender()

# ser = serial.Serial("/dev/ttyACM0", 115200, timeout = 1)

"""
controller mapping uses the right joystick to turn,
the left trigger to go forward, and the right trigger 
to go backwards.
"""

##TODO: turn and drive

try:
    while True:
        testing = False

        server.recieve() #receives data and assigns it to internal var
        data = server.decodeGround() #decodes w format string

        print(data)


        # if data[0] and len(data) == 1:
        #     #testing mode
        #     testing = True

        # else:
        #     testing = False

        # if not testing and len(data) != 3:

        #     rX = data[0]
        #     rY = data[1]
        #     lT = data[2]
        #     rT = data[3]

        #     lT += 1 #because it starts at -1 when not being pressed. now from 0-2
        #     rT += 1

        #     #drift reduction
        #     if rX < .1 and rX > -.1:
        #         rX = 0

        #     if rY < .1 and rY > -.1:
        #         rY=0

        #     print(f"{rX}, {rY}, {lT}, {rT}")

        #     #if not turning
        #     if rX == 0 and rY == 0: #if joystick is in default position, not turning
        #         #left trigger
        #         speed = min(.05*lT, .1)
        #         arduinoCom.sendSerial(False, speed, 'F')

        #         #right trigger
        #         speed = min(.05*rT, .1)
        #         arduinoCom.sendSerial(False, speed, 'B')
            
        #     #if turning. user not allowed to try to drive and turn, turning speed is determined on joystick movement
        #     else:
        #         rotation = AngleConverter()
        #         rotation.calc(rX, rY)
        #         print(f"angle: {rotation.angle}")
        #         arduinoCom.sendSerial(True, rotation.speed, rotation.angle)        


        #         # pwm = min(abs(rX*255), 255)
                
        #         # if rX < 0:
        #         #     arduinoCom.sendSerial(pwm, 'L')
        #         # else:
        #         #     arduinoCom.sendSerial(pwm, 'R')


        # elif testing:
        #     turning = data[0]
        #     speed = data[1]
        #     dir = data[2]
        #     arduinoCom.sendTest(turning, speed, dir)

        #     #if turning
        #     #if going straight
        

        # # while ser.in_waiting > 0:
        # #     response = ser.readline().decode().strip()
        # #     print(f"response: {response}")


except Exception as e:
    print("error: ")
    traceback.print_exc()
    server.close()