import time
import threading
import os

from Controller_Input import ControllerReader
from Network.TCP_Send import sendTCP
from Network.WifiPriority import SetAuto
from Testing_Mode_GUI import CubeRoverGUI


#set up class to handle controller inputs
global controller
controller = None
global wifi_connected
wifi_connected = False


def wifi_setup():

    #set up class for disabling automatic connection
    global diswifi
    global wifi_connected
    diswifi = SetAuto()
    serveraddress = ('10.42.0.1',5555)
    #serveraddress = ('192.168.1.174', 5555)
    #serveraddress = ('10.60.60.148', 5555)

    try:
        print("Checking for WiFi availability...")
        available = diswifi.available()
        while not available:
            print("Waiting for WiFi to become available...")
            time.sleep(1)
            available = diswifi.available()

        print("Attempting to connect to hotspot...")
        hotspot = diswifi.if_connect()
        while not hotspot:
            print("Waiting for hotspot connection...")
            time.sleep(1)
            hotspot = diswifi.if_connect()

        print("Connected to hotspot, disabling auto-connect...")
        diswifi.disable_auto()
        wifi_connected = True

        print("Attempting to establish TCP connection...")
        global tcp_client
        tcp_client = sendTCP(serveraddress)
        print("TCP connection established successfully")

    except Exception as e:
        print(f"Error in WiFi setup: {e}")
        diswifi.enable_auto()
        wifi_connected = False

def on_closing():
    print("Closing application...")
    # Clean up resources
    diswifi.enable_auto()
    if 'tcp_client' in globals():
        tcp_client.conn.close()
    # Destroy the GUI
    gui.gui.destroy()
    os._exit(0)


def check_controller():
    try:
        if gui.mode=='C' and wifi_connected:
            if controller.controller is not None:
                data = controller.get_input()
                if data is not None:
                    data = ['C'] + data
                    tcp_client.send(data)
            else:
                controller.connect()
    except Exception as e:
        print(f"Error in controller check: {e}")
    finally:
        if 'gui' in globals() and gui.gui.winfo_exists():
            gui.gui.after(250, check_controller)

def check_testing():
    try:
        if gui.mode == 'T' and wifi_connected:
            if not gui.command_line.empty():
                next_mes = gui.command_line.get()
                print("Sending testing command:", next_mes)
                tcp_client.send(next_mes)
    except Exception as e:
        print(f"Error in testing check: {e}")
    finally:
        if 'gui' in globals() and gui.gui.winfo_exists():
            gui.gui.after(200, check_testing)

def check_data():
    try:
        print("hi")
        print(tcp_client.receive())
    except:
        print("error receiving data")
    finally:
        if 'gui' in globals() and gui.gui.winfo_exists():
            gui.gui.after(200, check_data)

try:
    # Initialize WiFi first
    wifi_thread = threading.Thread(target=wifi_setup, args=(), daemon=True)
    wifi_thread.start()
    
    # Create GUI
    gui = CubeRoverGUI()

    # Set up the close handler
    gui.gui.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Initialize controller
    controller = ControllerReader()
    controller.connect()

    wifi_thread.join()
    pi_thread = threading.Thread(target=check_data, args=(), daemon=True)
    pi_thread.start()
    
    
    # Start the periodic checks
    check_controller()
    check_testing()

    
    # Run the GUI main loop
    gui.gui.mainloop()

except KeyboardInterrupt:
    print("\nCtrl+C pressed, shutting down...")
    on_closing()

except Exception as e:
    print(f"Error in main loop: {e}")
    on_closing()

finally:
    on_closing()  # Ensure cleanup happens



