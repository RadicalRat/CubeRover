import socket as sock
import PacketStruct as packet

class Network:
    def __init__(self,serveraddress):
        # Initializes the class to store the address, open a tcp socket, and bind the port
        self.address = serveraddress
        self.conn = sock.socket(sock.AF_INET, sock.SOCK_STREAM)

    def connect(self):
        try: #try to connect to the port
            self.conn.connect(self.address)
        except sock.error as error: #if failed, print the error
            print ("connection failed: ", error)
    
    def send(self, data):
        try: #send the data through the com port. Must be a string or a ControlPacket type
            self.conn.sendall(data.encode())
        except Exception as e: #prints error otherwise
            print("error!: ", e)
    def __bind__(self):
        self.conn.bind(self.serveraddress)
    

