from Controller_Input import ControllerReader
from Network.TCP_Send import TCP_Sender
import time

controller = ControllerReader() #initiliaze instance of class
tcp_client = TCP_Sender()

tcp_client.send_data((0,1,2,3))

# controller.connect() #connect controller

# while True:
#     if controller.controller is not None:
#         data = controller.get_input() #returns list

#         if data is not None:
#             tcp_client.send_data(data) #send data over wifi
#         else:
#             controller.connect() #try to connect controller again

#         time.sleep(.5) #eventually change to match slowest frequency




