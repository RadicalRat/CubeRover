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
        button = axis[data[0]] #changes axis number to character
        pos = data[1] * 255 #converts to pwm

        #print(pos)

        if button == "lT": #turn left
            arduinoCom.sendSerial(abs(pos), 'L')

        if button == "rT": #turn right
            arduinoCom.sendSerial(abs(pos), 'R')

        if button == "lY":
            if pos >= 0:
                arduinoCom.sendSerial(abs(pos), 'F')
            else:
                arduinoCom.sendSerial(abs(pos), 'B')

        if pos == 0:
            arduinoCom.sendSerial(0, 'F')

        while ser.in_waiting > 0:
            response = ser.readline().decode().strip()
            print(f"response: {response}")


except Exception as e:
    print("error: ")
    traceback.print_exc()
    server.close()





