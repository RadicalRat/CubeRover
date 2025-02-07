#to indiviudally test class functionality
from Controller_Input import ControllerReader

import time

controller = ControllerReader() #initiliaze instance of class

controller.connect() #connect controller

while True:
    if controller.controller is not None:
        data = controller.get_input() #returns list
        if data is not None:
            print(data)
    else:
        controller.connect() #try to connect controller again

    time.sleep(.05) #eventually change to match slowest frequency