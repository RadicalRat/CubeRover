import traceback
from pySerialTransfer import pySerialTransfer as pySer
import numpy as np

import Network.Networking as network
from InputConverter import ValConverter

serveraddress = ('0.0.0.0', 5555)
server = network.NetworkHost(serveraddress)
server.listenaccept()


#serial communication initialization
ser = pySer.SerialTransfer('/dev/ttyAMA0', baud=38400)
ser.open() 

"""
controller mapping uses the right joystick to turn,
the left trigger to go forward, and the right trigger 
to go backwards. Not moving anything or hitting the 
x button will send a stop command.
"""

#TODO: controller mode sends one char and 5 floats. testing mode shouldnt send that many. 
'''either modify networking to allow for two modes, 
modify it to allow for any number, or send testing
commands with zeroes for the extra values'''

try:
    while True:
        testing = False

        server.recieve() #receives data and assigns it to internal var
        data= []

        while not data:
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
            lT = data[3] + 1 #changes values from -1-1 to 0-2
            rT = data[4] + 1
            xbut = data[5]

            print(rX, rY, lT, rT)

            #drift reduction
            if rX < .1 and rX > -.1:
                rX = 0

            if rY < .1 and rY > -.1:
                rY = 0

            if xbut == 1: #send e stop command
                datasize = 0
                header = 'E'

                header_size = ser.tx_obj(header)
                datasize += header_size
                ser.send(datasize)


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
                vel1 = vel
                vel_size = ser.tx_obj(vel, datasize) - datasize
                datasize += vel_size
                datasize = ser.tx_obj(vel1, datasize)

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
            elif rX != 0 or rY != 0:
                output.angle_calc(rX, rY)
                print("hi")
                #TODO: once the IMU comes in, incorporate angle. for now only speed is used
                absVel = output.speed

                #right side, turning right
                #motor 1 and 2 are on the right side
                if rX > 0:
                    vel1 = 1 * absVel
                    vel2 = vel1

                    vel1 = vel1 - output.vel_calc(rT)

                    vel3 = absVel
                    vel4 = vel3

                else:
                    vel1 = absVel
                    vel2 = vel1

                    vel3 = 1 * absVel
                    vel4 = vel3

                    vel3 = vel3 - output.vel_calc(rT)

                


                header = 'V' #raw control of all motors

                datasize = 0

                datasize = ser.tx_obj(header, start_pos=datasize, val_type_override='c')
                datasize = ser.tx_obj(vel1, start_pos=datasize,val_type_override='f')
                datasize = ser.tx_obj(vel3, start_pos=datasize,val_type_override='f')


                ser.send(datasize)



        elif testing:
            if data[1] == 'V': #gives velocity and time 
                vel = data[2]
                time = data[3]

                #TODO: using positional control, but change to velocity control
                position = vel * time
                velencoder_count = vel * 28

                header = 'P'
                datasize = 0

                datasize = ser.tx_obj(header, start_pos=datasize, val_type_override='c')
                datasize = ser.tx_obj(position, start_pos=datasize, val_type_override='f')
                datasize = ser.tx_obj(velencoder_count, start_pos=datasize, val_type_override='f')


                ser.send(datasize)

            elif data[1] == 'P':
                distance = data[2]
                vel_encoder = data[3] * 28

                header = 'P'
                datasize = 0

                datasize = ser.tx_obj(header, start_pos=datasize, val_type_override='c')
                datasize = ser.tx_obj(distance, start_pos=datasize, val_type_override='f')
                datasize = ser.tx_obj(vel_encoder, start_pos=datasize, val_type_override='f')

                ser.send(datasize)

            elif data[1] == 'L':
                radius = data[2]

                if radius < 20.48:
                    radius = 20.48

                #dont have function on teensy for radius turning

                right_radius = radius + 20.48
                left_radius = radius - 20.48

                right_vel = 5/(left_radius*radius) #set turn speed to 5 cm/s
                left_vel = 5/(right_radius*radius)

                header = 'V'
                datasize = 0

                datasize = ser.tx_obj(header, start_pos=datasize, val_type_override='c')
                datasize = ser.tx_obj(right_vel, start_pos=datasize, val_type_override='f')
                datasize = ser.tx_obj(left_vel, start_pos=datasize, val_type_override='f')

                ser.send(datasize)
                
            elif data[1] == 'R':
                radius = data[2]

                if radius < 20.48:
                    radius = 20.48

                #dont have function on teensy for radius turning

                left_radius = radius + 20.48
                right_radius = radius - 20.48

                right_vel = 5/(left_radius*radius) #set turn speed to 5 cm/s
                left_vel = 5/(right_radius*radius)

                header = 'V'
                datasize = 0

                datasize = ser.tx_obj(header, start_pos=datasize, val_type_override='c')
                datasize = ser.tx_obj(right_vel, start_pos=datasize, val_type_override='f')
                datasize = ser.tx_obj(left_vel, start_pos=datasize, val_type_override='f')

                ser.send(datasize)


            #if turning
            #if going straight
        

        # # while ser.in_waiting > 0:
        # #     response = ser.readline().decode().strip()
        # #     print(f"response: {response}")


except Exception as e:
    print("error: ")
    traceback.print_exc()
    server.close()