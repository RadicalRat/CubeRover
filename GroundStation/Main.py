from Controller_Input import ControllerReader
from UDP_communication import UDPsender
import time

controller = ControllerReader() #initiliaze instance of class
udp_client = UDPsender()

controller.connect() #connect controller

try:
    while True:
        if controller.connected:
            data = controller.get_input() #returns list
            if data:
                UDPsender.send_data(data) #send data over wifi
        else:
            controller.connect() #try to connect controller again

        controller.check_quit()
        time.sleep(.05) #eventually change to match slowest frequency


except KeyboardInterrupt: #when program stopped, properly close programs
    controller.close()
    UDPsender.close()



