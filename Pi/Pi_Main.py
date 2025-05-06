import traceback
from pySerialTransfer import pySerialTransfer as pySer
import threading
import time as clock
import queue

import Network.Networking as network
import InputConverter as ic
from Packet_Send import packet

serveraddress = ('0.0.0.0', 5555)
server = network.NetworkHost(serveraddress)

#recieve
heartbeats = queue.Queue()
data_line = queue.Queue()

#send
serial_send = queue.Queue()

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
    def serial_data(stop):
        i = 0
        while not stop.is_set():
            # mes = serial.recv()
            # if mes:
            #     serial_send.put(mes)
            rover_data = [i+1, i+2,i+ 3,i+ 4,i+ 5,i+ 6,i+ 7,i+ 8,i+ 9,i+ 10,i+ 11, i+12, i+13,i+ 14,i+ 15,i+ 16,i+ 17,i+ 18,i+ 19,i+ 20]
            i+=1
            serial_send.put(rover_data)


    def comp_recv(stop):
        while not stop.is_set():
            data = []
            server.recieve()
            while not data:
                data = server.decodeGround()

            if data[0] == 'C' and data[1:6] == 100:
                heartbeats.put(data)
            else:
                data_line.put(data)



    serial_thread = threading.Thread(target=serial_data, args=(stop,), daemon=True)
    serial_thread.start()

    comp_thread = threading.Thread(target=comp_recv, args=(stop,), daemon=True)
    comp_thread.start()

    
    last_time = 0
    beat_interval = 5
    beat = [5.55]*20

    last_recv  = clock.time()

    while True:

        testing = False
        current_time = clock.time()

        #heartbeat function to test connectivity
        if current_time - last_time > beat_interval:
            server.send(beat)
            last_time = current_time

        if not heartbeats.empty():
            latest_heart = heartbeats.get()
            last_recv = clock.time()

        if current_time-last_recv > 7:
            print("connection closed")
            server.close()
            server.listenaccept()
            last_time = last_recv = clock.time()


        if not serial_send.empty():
            motion_data = serial_send.get()
            server.send(motion_data)


        if not data_line.empty():
            data = data_line.get()

            if data[0] == 'T': #testing mode
                testing = True

            elif data[0] == 'C':
                testing = False

            if not testing and data[1:6] == 5.55:
                heartbeats.put(data)
                print(data)

            elif not testing:

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

                    print(vel_enc, vel_enc2)

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

        clock.sleep(.005)
               

                

except (ConnectionResetError, BrokenPipeError) as w:
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
    comp_thread.join()
    #serial.ser.close()