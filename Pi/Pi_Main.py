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

global last_recv
last_recv = clock.time()

try:
    server.listenaccept()
    last_recv = clock.time()

    #serial communication initialization
    serial = packet('/dev/ttyAMA0', 38400)

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
            mes = serial.recv()
            if mes:
                serial_send.put(mes)



    def comp_recv(stop):
        global last_recv
        while not stop.is_set():
            if not server.connected:
                try:
                    print("trying to listen")
                    server.listenaccept()
                    last_recv = clock.time()
                except OSError:
                    print("error listneing")
                    clock.sleep(.5)
                    continue

            try:
                server.recieve()
                last_recv = clock.time()
            except (ConnectionError, OSError):
                server.close_client()
                continue

            data = None
            while data is None:
                data = server.decodeGround()

            last_recv = clock.time()

            if data[0] == 'C' and data[1] == 100 and data[2] == 100 and data[3] == 100:
                heartbeats.put(data)
                last_recv = clock.time()
            else:
                data_line.put(data)

            if clock.time()-last_recv > 7:
                server.close_client()



    serial_thread = threading.Thread(target=serial_data, args=(stop,), daemon=True)
    serial_thread.start()

    comp_thread = threading.Thread(target=comp_recv, args=(stop,), daemon=True)
    comp_thread.start()

    
    last_time = 0
    beat_interval = 5
    beat = [5.5]*20


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


        if not serial_send.empty():
            motion_data = serial_send.get()
            server.send(motion_data)


        if not data_line.empty():
            data = data_line.get()

            if data[0] == 'T': #testing mode
                testing = True

            elif data[0] == 'C':
                testing = False
                

            elif not testing:

                delay = 750.0

                #separate out buttons
                rX = data[1]
                rY = data[2] * -1 #up is negative, so changed to positive
                lT = data[3] + 1 #changes values from -1-1 to 0-2
                rT = data[4] + 1
                xbut = data[5]

                print(data)

                #drift reduction
                if rX < .1 and rX > -.1:
                    rX = 0

                if rY < .1 and rY > -.1:
                    rY = 0

                if xbut == 1: #send e stop command
                    serial.E()

                #if nothing is being pressed, send a stop command
                if lT == 0 and rT == 0 and rX == 0 and rY == 0:
                    
                    vel = float(0)
                    vel1 = vel

                    serial.V(vel, vel1, delay)

                #if turning
                elif (rT or lT) and (rX or rY):
                    if lT != 0:
                        trig = -1*lT
                    else:
                        trig = rT
                    angle, radius, vel1, vel2 = ic.turn_calc(rX, rY, trig)
                    serial.V(vel1, vel2, delay)

                #if right trigger is a non zero val, move forwards
                elif rT:
                    vel = abs(float(ic.linvel_calc(rT)))
                    vel1 = vel
                    
                    serial.V(vel, vel1, delay)
                    print("going")


                #if left trigger is non zero val, move backwards
                elif lT:
                    vel = -1*abs(float(ic.linvel_calc(lT)))
                    vel1 = vel

                    serial.V(vel, vel1, delay)
                

            #[t/c, position, radius, velocity, angle, time]
            elif testing:
                if data[4] == 1 and data[5] == 1: #position PID

                    pid = data[1:4]
                    serial.C(pid, 16)

                elif data[1] == 1 and data[5] == 1: #velocity PID
                    pid = data[2:5]
                    serial.C(pid, 0)

                elif data[1] == 1 and data[2] == 1: #turning pid
                    pid = data[3:]
                    serial.C(pid, 24) #fix later, probs not right


                elif data[3] != 0 and data[5] != 0: #speed and time command 
                    vel = data[3]
                    time = data[5] * 1000 #miliseconds

                    vel_enc = ic.testvel_calc(vel)

                    vel_enc2 = vel_enc

                    serial.V(vel_enc, vel_enc2, time)


                elif data[1] != 0: #position and velocity command
                    distance = data[1]
                    vel = data[3]

                    counts = ic.position_calc(distance)
                    vel_encoder = ic.testvel_calc(vel)

                    serial.P(counts, vel_encoder)


                elif data[2] != 0: #turn command
                    radius = data[2]*100 #cm
                    angle = data[4]
                    speed = data[3]

                    vel = ic.testvel_calc(speed)

                    serial.T(angle, radius, speed)

                elif all(c==0 for c in data[1:]): #if stop command do e stop
                    serial.E()

        clock.sleep(.005)
               

                

except (ConnectionResetError, BrokenPipeError) as w:
    pass
except KeyboardInterrupt:
    print("\nProgram terminated by user")
except Exception as e:
    print(f"An error occurred: {e}")
    traceback.print_exc()
finally:
    server.close_client()
    try:
        stop.set()
    except:
        pass
    serial_thread.join()
    comp_thread.join()
    serial.ser.close()