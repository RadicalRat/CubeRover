from UDP_Receiver import receive_UDP
from Serial_Sender import serialSender
import serial
import traceback

server = receive_UDP()
arduinoCom = serialSender()

axis = ["lX", "lY", "rX", "rY", "lT", "rT"]

ser = serial.Serial("/dev/ttyACM0", 115200, timeout = 1)

try:
    while True:
        data = server.receive_data()
        button = axis[data[0]-1] #changes axis number to character
        pos = data[1] #converts to pwm

        trig_normalized =(2 - pos + 1)*255
        pwm = pos*255
        #print(pos)

        if button == "lT": #turn left
            arduinoCom.sendSerial(trig_normalized, 'L')

        if button == "rT": #turn right
            arduinoCom.sendSerial(trig_normalized, 'R')

        if button == "lY":
            if pwm >= 0:
                arduinoCom.sendSerial(abs(pwm), 'F')
            else:
                arduinoCom.sendSerial(abs(pwm), 'B')

        while ser.in_waiting > 0:
            response = ser.readline().decode().strip()
            print(f"response: {response}")


except Exception as e:
    print("error: ")
    traceback.print_exc()
    server.close()





