import socket
import pickle

class receive_UDP:
    def __init__(self):
        self.ip = "0.0.0.0"
        self.port = 65432
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.ip, self.port))

    def receive_data(self):
        rec_data, _ = self.sock.recvfrom(1024) #buffer size in bytes
        data = pickle.loads(rec_data)
        motor_PWM = data * 255 #temporary for demo

        return motor_PWM
    
    def close(self):
        self.sock.close()
