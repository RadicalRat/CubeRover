import traceback
from pySerialTransfer import pySerialTransfer as pySer
import numpy as np

import Network.Networking as network
from InputConverter import ValConverter

serveraddress = ('0.0.0.0', 5555)
server = network.NetworkHost(serveraddress)


try:
    server.listenaccept()

    #serial communication initialization
    ser = pySer.SerialTransfer('/dev/ttyACM0', baud=38400)
    ser.open() 

    """
    controller mapping uses the right joystick to turn,
    the left trigger to go forward, and the right trigger 
    to go backwards. Not moving anything or hitting the 
    x button will send a stop command.
    """

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

            #print(rX, rY, lT, rT)

            #drift reduction
            if rX < .1 and rX > -.1:
                rX = 0

            if rY < .1 and rY > -.1:
                rY = 0

            if xbut == 1: #send e stop command
                print("stopped")
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


        # 1 for right, 0 for left
        # TODO: use input converter for this
        elif testing:
            if data[3] != 0 and data[5] != 0: #speed and time command 
                vel = data[3]
                time = data[5]
                print("vel", vel, time)

                #TODO: using positional control, but change to velocity control
                position = vel * time
                velencoder_count = vel * 537.7

                header = 'P'

                print(f"{header}, {position}, {velencoder_count}")
                datasize = 0

                datasize = ser.tx_obj(header, start_pos=datasize, val_type_override='c')
                datasize = ser.tx_obj(position, start_pos=datasize, val_type_override='f')
                datasize = ser.tx_obj(velencoder_count, start_pos=datasize, val_type_override='f')


                ser.send(datasize)

            elif data[1] != 0: #position and velocity command
                distance = data[1]
                vel_encoder = data[3] * 537.7

                header = 'P'
                datasize = 0

                print("position", distance, data[3])

                datasize = ser.tx_obj(header, start_pos=datasize, val_type_override='c')
                datasize = ser.tx_obj(distance, start_pos=datasize, val_type_override='f')
                datasize = ser.tx_obj(vel_encoder, start_pos=datasize, val_type_override='f')

                ser.send(datasize)

            #TODO: turn command on teensy
            elif data[2] != 0: #turn command
                radius = data[2]

                if radius < 20.48:
                    radius = 20.48

                if data[4]: #turn right
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

                else:

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

            elif all(c==0 for c in data[1:]): #if stop command do e stop
                header = 'E'
                datasize = ser.tx_obj(header, start_pos=0, val_type_override='c')

                ser.send(datasize)


                

        while ser.in_waiting > 0:
            response = ser.readline().decode().strip()
            server.send(response)


except KeyboardInterrupt:
    print("\nProgram terminated by user")
except Exception as e:
    print(f"An error occurred: {e}")
    traceback.print_exc()
finally:
    server.close()
    ser.close()