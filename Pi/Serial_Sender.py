import serial
import time

port = "/dev/ttyACM0"

class serialSender:
    def __init__(self):
        self.arduino = serial.Serial(port, 115200, timeout = 1)
        time.sleep(1)
        print("initialized")
        return

    def sendSerial(self, speed):
        self.arduino.write(f"{speed}\n".encode())

    def readSerial(self):
        print(self.arduino.readline().decode("ascii"))

    def serial_Close(self):
        self.close()



