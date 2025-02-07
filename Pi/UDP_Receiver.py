import socket
import pickle

class receive_UDP:
    def __init__(self):
        self.pi_ip = "10.42.0.1"
        self.port = 65432
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.pi_ip, self.port))

    def receive_data(self):
        rec_data, _ = self.sock.recvfrom(1024) #buffer size in bytes
        data = pickle.loads(rec_data)
        return data
    
    def close(self):
        self.sock.close()
