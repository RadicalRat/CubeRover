import socket as sock
import struct
import numpy as np

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
            self.conn.sendall(data)
            print("Data sent.")
        except sock.error as e: #prints error otherwise
            print("error!: ", e)

    def recieve(self):
        try: #recieve data through the port
            return self.conn.recv(1024)
        except sock.error as e: #prints error otherwise
            print("error!: ", e)
            

class NetworkHost:
    def __init__(self,serveraddress):
        #stores server address, and binds it to the socket
        self.address = serveraddress
        self.conn = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        self.conn.bind(self.address)

    def listenaccept(self):
        self.conn.listen(1)
        print("Listening...")
        self.client,self.clientadr = self.conn.accept()
        print("Client Connected:", self.clientadr)
    
    def recieve(self):
        try:
            return self.client.recv(1024)
        except sock.error as e:
            print("error!", e)

    def send(self, data):
        try: #send the data through the com port. Must be a string or a ControlPacket type
            self.client.sendall(data)
        except sock.error as e: #prints error otherwise
            print("error!: ", e)
    def check(self):
        flag = self.conn.recv(1024, sock.MSG_PEEK)
        if (flag):
            return True
        else:
            return False
    

def Decoder(data):
    header = struct.unpack('1c',data[:1])[0].decode() # unpacks header
    print(header)
    match header: # uses header to unpack float data
        case 'R':
            data = struct.unpack('4f',data[1:])
        case 'V':
            data = struct.unpack('1f',data[1:])
        case 'D':
            data = struct.unpack('2f',data[1:])

    packet = (header[0], data) #stores the data in a set and returns
    return packet

def Encoder(data):
    format_string = f'=1c{len(data)-1}f'
    encodedData = struct.pack(format_string,*data)
    return encodedData