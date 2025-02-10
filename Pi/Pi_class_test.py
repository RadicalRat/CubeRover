from UDP_Receiver import receive_UDP
from Serial_Sender import serialSender

server = receive_UDP()
arduinoCom = serialSender()

axis = ["lX", "lY", "rX", "rY", "lT", "rT"]

try:
    while True:
        data = server.receive_data()
        button = axis[data[0]] #changes axis number to character
        pos = data[1]

        if button == "lT": #turn left
            arduinoCom.sendSerial(pos, 'L')

        if button == "rT": #turn right
            arduinoCom.sendSerial(pos, 'R')

        if button == "lY":
            if pos >= 0:
                arduinoCom.sendSerial(pos, 'F')
            else:
                arduinoCom.sendSerial(pos, 'B')


except:
    server.close()





