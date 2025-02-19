#using UDP protocol because its fast and doesn't have to be super reliable

import socket
import pickle #converts python objects to bytes

pi_ip = "10.42.0.1" #rpi5
#pi_ip = "192.168.1.100" #my pi
comp_Port = 65432

class UDPsender:
    def __init__(self):
        self.host = pi_ip
        self.port = comp_Port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_data(self, data):
        try:
            message = pickle.dumps(data) #to send more versatile data
            self.sock.sendto(message, (self.host, self.port))
        except Exception as e:
            print(f"Error sending data: {e}")
    
    def close(self):
        self.sock.close()
