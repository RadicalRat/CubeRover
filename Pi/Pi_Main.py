import traceback
from pySerialTransfer import pySerialTransfer as pySer
import numpy as np

import Network.Networking as network
from InputConverter import ValConverter

serveraddress = ('0.0.0.0', 5555)
server = network.NetworkHost(serveraddress)
server.listenaccept()

#TODO: change networking back to allow less or mroe than four floats

#serial communication initialization
ser = pySer.SerialTransfer('/dev/ttyAMA0', baud=38400)
ser.open() 

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

        if data[0] == 'T': #testing mode
            testing = True

        elif data[0] == 'C':
            testing = False


        if not testing:

            output = ValConverter()

            #separate out buttons
            rX = data[1]
            rY = data[2]
            lT = data[2] + 1 #changes values from -1-1 to 0-2
            rT = data[3] + 1

            #drift reduction
            if rX < .1 and rX > -.1:
                rX = 0

            if rY < .1 and rY > -.1:
                rY = 0

            #if nothing is being pressed, send a stop command
            if lT == 0 and rT == 0 and rX == 0 and rY == 0:
                datasize = 0
                header = 'V' #raw control of motors
                """the tx_obj thing returns the size of whatever is put into
                it and also links the thing in it to an internal message to
                send when the send function is called. you have to keep track
                of current datasize because objects are added at the end of 
                datasize."""
                header_size = ser.tx_obj(header)
                datasize += header_size

                vel = float(0)
                vel_size = ser.tx_obj(vel, datasize) - datasize
                datasize += vel_size
                datasize = ser.tx_obj(vel, datasize)

                ser.send(datasize)

            #if right trigger is a non zero val, move forwards
            elif rT:
                vel = float(output.vel_calc(rT))
                vel1 = vel
                header = 'V' #speed control

                datasize = 0
                
                datasize = ser.tx_obj(header, start_pos=datasize, val_type_override='c')
                datasize = ser.tx_obj(vel, start_pos=datasize,val_type_override='f')
                datasize = ser.tx_obj(vel1, start_pos=datasize,val_type_override='f')

                ser.send(datasize)

            #if left trigger is non zero val, move backwards
            elif lT:
                vel = -1*float(output.vel_calc(lT))
                vel1 = vel
                header = 'V' #speed control

                datasize = 0
                
                datasize = ser.tx_obj(header, start_pos=datasize, val_type_override='c')
                datasize = ser.tx_obj(vel, start_pos=datasize,val_type_override='f')
                datasize = ser.tx_obj(vel1, start_pos=datasize,val_type_override='f')

                ser.send(datasize)

            #if turning
            elif rX or rY:
                output.angle_calc(rX, rY)
                print(output.angle)
                #TODO: once the IMU comes in, incorporate angle. for now only speed is used
                absVel = output.speed

                #right side, turning right
                #im defining motor 1 and 2 to be on the right side for now
                if output.angle > -1*np.pi/2 and output.angle < np.pi/2:
                    vel1 = -1 * absVel
                    vel2 = vel1

                    vel3 = absVel
                    vel4 = vel3

                else:
                    vel1 = absVel
                    vel2 = vel1

                    vel3 = -1 * absVel
                    vel4 = vel3

                header = 'V' #raw control of all motors

                datasize = 0

                datasize = ser.tx_obj(header, start_pos=datasize, val_type_override='c')
                datasize = ser.tx_obj(vel1, start_pos=datasize,val_type_override='f')
                datasize = ser.tx_obj(vel3, start_pos=datasize,val_type_override='f')


                ser.send(datasize)



        elif testing:
            turning = data[0]
            speed = data[1]
            dir = data[2]

            #if turning
            #if going straight
        

        # # while ser.in_waiting > 0:
        # #     response = ser.readline().decode().strip()
        # #     print(f"response: {response}")


except Exception as e:
    print("error: ")
    traceback.print_exc()
    server.close()