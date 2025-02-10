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

        print(pos)

        if button == "lT": #turn left
            arduinoCom.sendSerial(abs(pos), 'L')

        if button == "rT": #turn right
            arduinoCom.sendSerial(abs(pos), 'R')

        if button == "lY":
            if pos >= 0:
                arduinoCom.sendSerial(abs(pos), 'F')
            else:
                arduinoCom.sendSerial(abs(pos), 'B')


except:
    server.close()





