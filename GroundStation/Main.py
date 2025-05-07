import time
import threading
import queue

from Controller_Input import ControllerReader
from Network.Networking import NetworkClient
from Network.WifiPriority import SetAuto
from Testing_Mode_GUI import CubeRoverGUI


controller = None
global autooff
autooff = False

shutdown = threading.Event()
controller = None
diswifi = SetAuto()

send_line = queue.Queue()


# def wifi_setup():
serveraddress = ('10.42.0.1',5555)
print("Attempting to establish TCP connection...")
tcp_client = NetworkClient(serveraddress)

def wifi_setup():
    while not tcp_client.connected and not shutdown.is_set():
        try:
            tcp_client.connect()
            time.sleep(.2)
        except Exception as e:
            print(f"Error in WiFi setup: {e}")
            tcp_client.close()
        except SystemExit:
            raise

def on_closing():
    if shutdown.is_set():
        return
    print("Closing application...")
    # Clean up resources
    shutdown.set()
    global autooff
    try:
        diswifi.enable_auto()
    except:
        pass
    if 'tcp_client' in globals():
        tcp_client.connected = False
        try:
            tcp_client.close()
        except:
            pass
    # Destroy the GUI
    gui.gui.quit()



def check_input():
    try:
        if gui.mode=='C' and tcp_client.connected and not shutdown.is_set():
            if controller.controller is not None:
                data = controller.get_input()
                if data is not None:
                    data = ['C'] + data
                    tcp_client.send(data)
            else:
                controller.connect()

        elif gui.mode == 'T' and tcp_client.connected:
            if not gui.command_line.empty():
                next_mes = gui.command_line.get()
                send_line.put(next_mes)

    except Exception as e:
        print(f"Error in input check: {e}")
    finally:
        if gui.gui.winfo_exists() and not shutdown.is_set():
            gui.gui.after(250, check_input)


def check_data():
    last_recv = time.time()
    while not tcp_client.connected:
        time.sleep(.2)
    while tcp_client.connected and gui.gui.winfo_exists() and not shutdown.is_set(): 
        try:
            data = tcp_client.receive()
            current_time = time.time()
            if data is None:
                break
            if all(x == 5.5 for x in data):
                last_recv = time.time()
                beat = ['C', 100, 100, 100, 100, 100]
                send_line.put(beat)
            else:
                gui.telemetry_data = data
                #print(gui.telemetry_data)

            if current_time - last_recv > 20:
                while not tcp_client.connected:
                    try:
                        tcp_client.connect()
                        time.sleep(.2)
                    except:
                        tcp_client.close()

        except Exception as e:
            print("error receiving data")
            break

        time.sleep(.05)

def pi_send():
    try:
        if tcp_client.connected and not send_line.empty():
            next_mes = send_line.get()
            tcp_client.send(next_mes)
    except:
        print("error in sending to pi")
    finally:
        if gui.gui.winfo_exists() and not shutdown.is_set():
            gui.gui.after(250, pi_send)

def check_autoconnect():
    global autooff
    try:
        if gui.os_mode == "W" and not autooff and not shutdown.is_set():
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
        if gui.gui.winfo_exists() and not shutdown.is_set():
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
    check_input()
    check_autoconnect()
    pi_send()

    
    # Run the GUI main loop
    gui.gui.mainloop()

except KeyboardInterrupt:
    print("\nCtrl+C pressed, shutting down...")
    on_closing()

except Exception as e:
    print(f"Error in main loop: {e}")
    on_closing()





