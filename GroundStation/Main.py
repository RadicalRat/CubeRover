import time
import threading
import os

from Controller_Input import ControllerReader
from Network.Networking import NetworkClient
from Network.WifiPriority import SetAuto
from Testing_Mode_GUI import CubeRoverGUI


#set up class to handle controller inputs
global controller
controller = None
global wifi_connected
wifi_connected = False
global autooff
autooff = False


# def wifi_setup():
serveraddress = ('10.42.0.1',5555)
#serveraddress = ('192.168.1.174', 5555)
#serveraddress = ('10.60.60.148', 5555)


print("Attempting to establish TCP connection...")
global tcp_client
tcp_client = NetworkClient(serveraddress)

def wifi_setup():
    while not tcp_client.connected:
        try:
            tcp_client.connect()
            time.sleep(.2)
        except Exception as e:
            print(f"Error in WiFi setup: {e}")
            tcp_client.close()
        except SystemExit:
            raise

def on_closing():
    print("Closing application...")
    # Clean up resources
    global autooff
    if autooff:
        diswifi.enable_auto()
    if 'tcp_client' in globals():
        tcp_client.connected = False
        tcp_client.close()
    # Destroy the GUI
    if 'gui' in globals():
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
    while tcp_client.connected and gui.gui.winfo_exists(): 
        try:
            data = tcp_client.receive()
            if data is None:
                break
            gui.telemetry_data = data
            print(gui.telemetry_data)
        except Exception as e:
            print("error receiving data")
            break

        time.sleep(.05)

def check_autoconnect():
    global autooff, diswifi
    try:
        diswifi = SetAuto()
        if gui.os_mode == "W" and not autooff:
            if not diswifi.available():
                pass
            elif not diswifi.if_connect():
                pass
            else:
                diswifi.disable_auto()
                autooff = True

    except Exception as e:
        print("Error... Change to Linux mode")
    finally:
        if 'gui' in globals() and gui.gui.winfo_exists():
            gui.gui.after(500, check_autoconnect)


try:

    wifi_thread = threading.Thread(target=wifi_setup, args=(), daemon=True)
    wifi_thread.start()
    
    # Create GUI
    gui = CubeRoverGUI()

    # Set up the close handler
    gui.gui.protocol("WM_DELETE_WINDOW", on_closing)

    pi_thread = threading.Thread(target=check_data, args=(), daemon=True)
    pi_thread.start()

    # Initialize controller
    controller = ControllerReader()
    controller.connect()
    
    # Start the periodic checks
    check_controller()
    check_testing()
    check_autoconnect()

    
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



