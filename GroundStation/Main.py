import time

from Controller_Input import ControllerReader
from Network.TCP_Send import sendTCP

#set up class to handle controller inputs
controller = ControllerReader() #initiliaze instance of class
controller.connect()

#setting up wifi protocol
serveraddress = ('10.42.0.1',5555)
#serveraddress = ('192.168.1.174', 5555)
#serveraddress = ('10.60.60.148', 5555)
tcp_client = sendTCP(serveraddress)

""" TODO: add the heading back in but instead of ID number make it
'C' for controller or 'T' for testing mode

TODO: make wifi wait longer with a message that its trying to connect,
add an interupt to make exiting easier
"""

while True:
    if controller.controller is not None:
        data = controller.get_input() #returns list of four

        if data is not None:
            tcp_client.send(data) #send data over wifi

    else:
        controller.connect() #try to connect controller if not connected

    time.sleep(.5) #eventually change to match slowest frequency

