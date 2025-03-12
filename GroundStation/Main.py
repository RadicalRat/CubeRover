from Controller_Input import ControllerReader
from Network.TCP_Send import sendTCP
import time

#set up class to handle controller inputs
controller = ControllerReader() #initiliaze instance of class
controller.connect()

#setting up wifi protocol
serveraddress = ('10.42.0.1',5555)
tcp_client = sendTCP(serveraddress)

while True:
    if controller.controller is not None:
        data = controller.get_input() #returns list

        if data is not None:
            tcp_client.send(data) #send data over wifi

    else:
        controller.connect() #try to connect controller if not connected

    time.sleep(.5) #eventually change to match slowest frequency

