import time

from Controller_Input import ControllerReader
from Network.TCP_Send import sendTCP
from Network.WifiPriority import SetAuto

#set up class to handle controller inputs
controller = ControllerReader() #initiliaze instance of class
controller.connect()
#set up class for disabling automatic connection
diswifi = SetAuto()
#setting up wifi protocol
serveraddress = ('10.42.0.1',5555)
#serveraddress = ('192.168.1.174', 5555)
#serveraddress = ('10.60.60.148', 5555)

#check if hotspot is available
available = diswifi.available()

try:
    while not available:
        avaiable = diswifi.available()

    hotspot = diswifi.if_connect()

    while not hotspot:
        print("not connected to wifi")
        hotspot = diswifi.if_connect()

    diswifi.disable_auto() #disable autoconnections to other networks

except Exception as e:
    diswifi.enable_auto()

#try to open server connection
try:
    tcp_client = sendTCP(serveraddress)
except:
    print("couldnt establish server")

""" TODO: add the heading back in but instead of ID number make it
'C' for controller or 'T' for testing mode

TODO: make wifi wait longer with a message that its trying to connect,
add an interupt to make exiting easier
"""

'''rover_gui = CubeRoverGUI()
rover_gui.run_GUI()'''


try:
    while True:
        
        if controller.controller is not None:
            data = controller.get_input() #returns list of four

            if data is not None:
                tcp_client.send(data) #send data over wifi

        else:
            controller.connect() #try to connect controller if not connected

        time.sleep(.02) #eventually change to match slowest frequency

except Exception as e:
    print(e)
    diswifi.enable_auto()
    tcp_client.conn.close()


finally:
    diswifi.enable_auto()
    tcp_client.conn.close()



#This is how to create and call the GUI, not sure how we will differentiate between controller and testing mode
'''rover_gui = CubeRoverGUI()
rover_gui.run_GUI()'''

