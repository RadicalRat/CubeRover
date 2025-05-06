import traceback
from pySerialTransfer import pySerialTransfer as pySer
import threading
import time

import Network.Networking as network
import InputConverter as ic
from Packet_Send import packet

serveraddress = ('0.0.0.0', 5555)
server = network.NetworkHost(serveraddress)


try:
    server.listenaccept()

    #serial communication initialization
    #serial = packet('/dev/ttyAMA0', 38400)

    stop = threading.Event()

    """
    controller mapping uses the right joystick to turn,
    the left trigger to go back, and the right trigger 
    to go forward. Not moving anything or hitting the 
    x button will send a stop command.
    """
    def motion_data(stop):
        i = 0
        while not stop.is_set():
            #rover_data = serial.recv()
            rover_data = [i+1, i+2,i+ 3,i+ 4,i+ 5,i+ 6,i+ 7,i+ 8,i+ 9,i+ 10,i+ 11, i+12, i+13,i+ 14,i+ 15,i+ 16,i+ 17,i+ 18,i+ 19,i+ 20]
            i+=1
            if len(rover_data) != 0:
                server.send(rover_data)

            time.sleep(1)

    serial_thread = threading.Thread(target=motion_data, args=(stop,), daemon=True)
    serial_thread.start()

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
        print(data)

        if not testing:

            delay = 750.0

            #separate out buttons
            rX = data[1]
            rY = data[2] * -1 #up is negative, so changed to positive
            lT = data[3] + 1 #changes values from -1-1 to 0-2
            rT = data[4] + 1
            xbut = data[5]

            #drift reduction
            if rX < .1 and rX > -.1:
                rX = 0

            if rY < .1 and rY > -.1:
                rY = 0

            if xbut == 1: #send e stop command
                #serial.E()
                pass

            #if nothing is being pressed, send a stop command
            if lT == 0 and rT == 0 and rX == 0 and rY == 0:
                
                vel = float(0)
                vel1 = vel

                #serial.V(vel, vel1, delay)

            #if turning
            elif (rT or lT) and (rX or rY):
                if lT != 0:
                    trig = -1*lT
                else:
                    trig = rT
                angle, radius, vel1, vel2 = ic.turn_calc(rX, rY, trig)
                print(angle, radius, vel1, vel2)
                #serial.V(vel1, vel2, delay)

            #if right trigger is a non zero val, move forwards
            elif rT:
                vel = abs(float(ic.linvel_calc(rT)))
                vel1 = vel
                
                #serial.V(vel, vel1, delay)


            #if left trigger is non zero val, move backwards
            elif lT:
                vel = -1*abs(float(ic.linvel_calc(lT)))
                vel1 = vel
                print(vel, vel1)

                #serial.V(vel, vel1, delay)
            

        #[t/c, position, radius, velocity, angle, time]
        elif testing:
            if data[4] == 1 and data[5] == 1: #position PID

                pid = data[1:4]
                #serial.C(pid, 16)

            elif data[1] == 1 and data[5] == 1: #velocity PID
                pid = data[2:5]
                #serial.C(pid, 0)

            elif data[1] == 1 and data[2] == 1: #turning pid
                pid = data[3:]
                #serial.C(pid, 24) #fix later, probs not right


            elif data[3] != 0 and data[5] != 0: #speed and time command 
                vel = data[3]
                time = data[5] * 1000 #miliseconds

                vel_enc = ic.testvel_calc(vel)

                vel_enc2 = vel_enc

                #serial.V(vel_enc, vel_enc2, time)


            elif data[1] != 0: #position and velocity command
                distance = data[1]
                vel = data[3]

                counts = ic.position_calc(distance)
                vel_encoder = ic.testvel_calc(vel)

                #serial.P(counts, vel_encoder)


            elif data[2] != 0: #turn command
                radius = data[2]*100 #cm
                angle = data[4]
                speed = data[3]

                vel = ic.testvel_calc(speed)

                #serial.T(angle, radius, speed)

            elif all(c==0 for c in data[1:]): #if stop command do e stop
                #serial.E()
                pass

                

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
    stop.set()
    serial_thread.join()
    #serial.ser.close()