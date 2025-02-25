from UDP_Receiver import receive_UDP
from Serial_Sender import serialSender
import serial
import traceback

server = receive_UDP()
arduinoCom = serialSender()

ser = serial.Serial("/dev/ttyACM0", 115200, timeout = 1)

try:
    while True:
        #right joystick controls turning, left trig is forward, right is backwards
        rX, rY, lT, rT = server.receive_data()
        lT += 1 #because it starts at -1 when not being pressed
        rT += 1

        print(f"{rX}, {rY}, {lT}, {rT}")

        #right joystick x axis, simplified logic
        if rX < .1 and rX > -.1:
            arduinoCom.sendSerial(0, 'F')
        else:
            pwm = min(abs(rX*255), 255)
            
            if rX < 0:
                arduinoCom.sendSerial(pwm, 'L')
            else:
                arduinoCom.sendSerial(pwm, 'R')

        #left trigger
        pwm = min(abs(lT), 255)
        arduinoCom.sendSerial(pwm, 'F')

        #right trigger
        pwm = min(abs(pwm), 255)
        arduinoCom.sendSerial(pwm, 'B')
        

        while ser.in_waiting > 0:
            response = ser.readline().decode().strip()
            print(f"response: {response}")


except Exception as e:
    print("error: ")
    traceback.print_exc()
    server.close()





