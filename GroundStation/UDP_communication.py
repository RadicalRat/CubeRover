#using UDP protocol because its fast and doesn't have to be super reliable

import socket
import pickle #converts python objects to bytes

pi_ip = "10.42.0.1"
comp_Port = 65432

class UDPsender:
    def _init_(self, host = pi_ip, port = comp_Port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_data(self, data):
        try:
            message = pickle.dumps(data) #to send more versatile data
            self.sock.sendto(message.encode(), (self.host, self.port))
        except Exception as e:
            print(f"Error sending data: {e}")
    
    def close(self):
        self.sock.close()
