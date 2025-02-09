from UDP_Receiver import receive_UDP
from Serial_Sender import serialSender

# server = receive_UDP()

# try:
#     while True:
#         data = server.receive_data()
#         print(data)

# except:
#     server.close()

arduino_serial = serialSender()
arduino_serial.sendSerial(5)
arduino_serial.sendSerial(6)


