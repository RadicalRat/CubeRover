import socket as sock
import struct

class NetworkClient:
    def __init__(self,serveraddress):
        # Initializes the class to store the address, open a tcp socket, and bind the port
        self.address = serveraddress
        self.conn = sock.socket(sock.AF_INET, sock.SOCK_STREAM)

    def connect(self):
        try: #try to connect to the port
            self.conn.connect(self.address)
            print("Port connected.")
        except sock.error as error: #if failed, print the error
            print ("connection failed: ", error)
            exit()
    
    def send(self, data):
        try: #send the data through the com port. Must be a string or a ControlPacket type
            self.conn.sendall(data.encode())
            print("Data sent.")
        except sock.error as e: #prints error otherwise
            print("error!: ", e)

    def recieve(self):
        try: #recieve data through the port
            return self.conn.recv(1024).decode()
        except sock.error as e: #prints error otherwise
            print("error!: ", e)

    def close(self):
        self.conn.close()
            

class NetworkHost:
    def __init__(self,serveraddress):
        #stores server address, and binds it to the socket
        self.address = serveraddress
        self.streamData = ()
        self.conn = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        self.conn.bind(self.address)

    def listenaccept(self):
        self.conn.listen(1)
        print("Listening...")
        self.client,self.clientadr = self.conn.accept()
        print("Client Connected:", self.clientadr)
    
    def recieve(self):
        try:
            self.streamData = self.client.recv(1024)
        except sock.error as e:
            print("error!", e)

    def send(self, data):
        try: #send the data through the com port. Must be a string or a ControlPacket type
            self.client.sendall(data.encode())
        except sock.error as e: #prints error otherwise
            print("error!: ", e)

    def decodeGround(self): #decode incoming data from computer to Pi
        #format_string = f'={int((len(self.streamData) - len(self.streamData) % 4) /4)}f'
        format_string = '=1c4f'
        mes = struct.unpack(format_string, self.streamData)
        data = [mes[0].decode(), mes[1], mes[2], mes[3], mes[4]]
        return data
    
    def close(self):
        self.conn.close()