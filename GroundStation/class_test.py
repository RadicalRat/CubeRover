#to indiviudally test class functionality
from Controller_Input import ControllerReader
from UDP_communication import UDPsender
import time

controller = ControllerReader() #initiliaze instance of class
controller.connect() #connect controller

server = UDPsender()


while True:
    if controller.controller is not None:
        data = controller.get_input() #returns list
        print(data)
        
        if data is not None:
            server.send_data(data)
    else:
        controller.connect() #try to connect controller again

    time.sleep(.05) #eventually change to match slowest frequency