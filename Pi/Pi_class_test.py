from UDP_Receiver import receive_UDP
from Serial_Sender import serialSender
from Angle_Converter import AngleConverter
import serial
import traceback

server = receive_UDP()
arduinoCom = serialSender()

ser = serial.Serial("/dev/ttyACM0", 115200, timeout = 1)


try:
    while True:
        testing = False

        #right joystick controls turning, left trig is forward, right is backwards
        data = server.receive_data()

        if data:
            #testing mode
            testing = True

        elif not data:
            testing = False

        if not testing and len(data) != 3:

            rX = data[0]
            rY = data[1]
            lT = data[2]
            rT = data[3]

            lT += 1 #because it starts at -1 when not being pressed. now from 0-2
            rT += 1

            print(f"{rX}, {rY}, {lT}, {rT}")

            #drift reduction
            if rX < .1 and rX > -.1:
                rX = 0

            if rY < .1 and rY > -.1:
                rY=0

            #right joystick
            if rX == 0 and rY == 0: #if joystick is in default position
                arduinoCom.sendSerial(False, 0) #dont move -> inputs: is it turning, speed, direction
            else:
                rotation = AngleConverter()
                rotation.calc(rX, rY)
                arduinoCom.sendSerial(True, rotation.speed, rotation.angle)        


                # pwm = min(abs(rX*255), 255)
                
                # if rX < 0:
                #     arduinoCom.sendSerial(pwm, 'L')
                # else:
                #     arduinoCom.sendSerial(pwm, 'R')

            #left trigger
            speed = min(.05*lT, .1)
            arduinoCom.sendSerial(False, speed, 'F')

            #right trigger
            speed = min(.05*rT, .1)
            arduinoCom.sendSerial(False, speed, 'B')

        elif testing:
            turning = data[0]
            speed = data[1]
            dir = data[2]
            arduinoCom.sendTest(turning, speed, dir)

            #if turning
            #if going straight
        

        # while ser.in_waiting > 0:
        #     response = ser.readline().decode().strip()
        #     print(f"response: {response}")


except Exception as e:
    print("error: ")
    traceback.print_exc()
    server.close()





