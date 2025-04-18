import time
import threading

from Controller_Input import ControllerReader
from Network.TCP_Send import sendTCP
from Network.WifiPriority import SetAuto
from integrated_gui import CubeRoverGUI
from queue import Queue, Empty

commands = Queue()
testing = True
gui = None

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
        available = diswifi.available()

    hotspot = diswifi.if_connect()

    while not hotspot:
        print("not connected to wifi")
        hotspot = diswifi.if_connect()

    diswifi.disable_auto() #disable autoconnections to other networks

except Exception as e:
    print(f"Error in setup: {e}")
    diswifi.enable_auto()

#try to open server connection
try:
    tcp_client = sendTCP(serveraddress)
except Exception as e:
    print(f"Couldn't establish server: {e}")


def process_commands():
    global testing  # Need to declare as global to modify it
    while True:
        try:
            # Get command from GUI if available
            if gui:
                command = gui.send_command()
                if command:
                    commands.put(command)
            
            # Process commands from queue
            command = commands.get(timeout=0.1)
            if command:
                print(f"Processing command: {command}")
                tcp_client.send(command)
                # Update testing mode based on command type
                if command[0] == 'C':
                    testing = False
                else:
                    testing = True
            
            # If in controller mode, handle controller input
            if not testing:
                controller_handling()
                
        except Empty:
            continue
        except Exception as e:
            print(f"Error processing command: {e}")


def controller_handling(): #thread function
    #set up class to handle controller inputs
    controller = ControllerReader() #initiliaze instance of class
    controller.connect()


    try:
        while True:
            if controller.controller is not None:
                data = controller.get_input() #returns list of five

                if data is not None:
                    tcp_client.send(data) #send data over wifi

            else:
                controller.connect() #try to connect controller if not connected

            time.sleep(.5) #eventually change to match slowest frequency

    except Exception as e:
        print(f"Error in main loop: {e}")
        diswifi.enable_auto()
        tcp_client.conn.close()

    finally:
        diswifi.enable_auto()
        tcp_client.conn.close()




input_thread = threading.Thread(target = process_commands, args=(), daemon=True)
input_thread.start()

gui = CubeRoverGUI()
gui.gui.mainloop()
