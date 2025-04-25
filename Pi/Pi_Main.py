import traceback
from pySerialTransfer import pySerialTransfer as pySer
from datetime import datetime

import Network.Networking as network
import InputConverter as ic
from Packet_Send import packet

serveraddress = ('0.0.0.0', 5555)
server = network.NetworkHost(serveraddress)


try:
    server.listenaccept()

    #serial communication initialization
    serial = packet('/dev/ttyAMA0', 38400)

    """
    controller mapping uses the right joystick to turn,
    the left trigger to go back, and the right trigger 
    to go forward. Not moving anything or hitting the 
    x button will send a stop command.
    """

    while True:
        testing = False

        server.recieve() #receives data and assigns it to internal var
        data= []

        while not data:
            data = server.decodeGround() #decodes w format string

        #for time stamp
        if data[0] == 'S':
            print(data)
            print(datetime.now().strftime('%H:%M:%S.%f'))

        if data[0] == 'T': #testing mode
            testing = True

        elif data[0] == 'C':
            testing = False

        print(data)


        if not testing:

            delay = 750.0

            #separate out buttons
            rX = data[1]
            rY = data[2]
            lT = data[3] + 1 #changes values from -1-1 to 0-2
            rT = data[4] + 1
            xbut = data[5]

            #drift reduction
            if rX < .1 and rX > -.1:
                rX = 0

            if rY < .1 and rY > -.1:
                rY = 0

            if xbut == 1: #send e stop command
                print("stopped")
                serial.E()


            #if nothing is being pressed, send a stop command
            if lT == 0 and rT == 0 and rX == 0 and rY == 0:
                
                vel = float(0)
                vel1 = vel

                serial.V(vel, vel1, delay)

            #if right trigger is a non zero val, move forwards
            elif rT:
                vel = float(ic.linvel_calc(rT))
                vel1 = vel
                
                serial.V(vel, vel1, delay)


            #if left trigger is non zero val, move backwards
            elif lT:
                vel = -1*float(ic.linvel_calc(lT))
                vel1 = vel

                serial.V(vel, vel1, delay)
            
            #if turning
            elif rX != 0 or rY != 0:
                angle, radius, speed, vel1, vel2  = ic.turn_calc(rX, rY)
                serial.V(vel1, vel2, delay)

        #[t/c, position, radius, velocity, angle, time]
        elif testing:
            if data[4] == 1 and data[5] == 1: #velocity PID

                pid = data[1:3]
                serial.C(pid, 0)


            elif data[3] != 0 and data[5] != 0: #speed and time command 
                vel = data[3]
                time = data[5]
                print("vel", vel, time)

                #TODO: using positional control, but change to velocity control
                position = vel * time
                velencoder_count = vel * 537.7
                velencoder2 = velencoder_count


                serial.V(velencoder_count, velencoder2, time)


            elif data[1] != 0: #position and velocity command
                distance = data[1]
                vel_encoder = data[3] * 537.7

                print("position", distance, data[3])

                serial.P(distance, vel_encoder)


            elif data[2] != 0: #turn command
                radius = data[2]
                angle = [4]
                speed = [3]

                serial.T(angle, radius, speed)

            elif all(c==0 for c in data[1:]): #if stop command do e stop
                serial.E()
                

except (ConnectionResetError, BrokenPipeError) as w:
    try:
        server.conn.close()
        server.listenaccept()
    except:
        pass
except KeyboardInterrupt:
    print("\nProgram terminated by user")
except Exception as e:
    print(f"An error occurred: {e}")
    traceback.print_exc()
finally:
    server.close()
    serial.ser.close()