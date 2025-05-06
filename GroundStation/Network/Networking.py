import socket as sock
import struct

class NetworkClient:
    def __init__(self,serveraddress):
        # Initializes the class to store the address, open a tcp socket, and bind the port
        self.address = serveraddress
        self.streamData = ()
        self.conn = None
        self.connected = False

    def connect(self):
        try: 
            #close any old broken sockets
            if self.conn is not None:
                try:
                    self.conn.close()
                except:
                    pass
            #create a new socket
            self.conn = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
            self.conn.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)
            self.conn.settimeout(3)
            self.conn.connect(self.address)
            self.conn.settimeout(None)

            print("Port connected.")
            self.connected = True
        except sock.timeout:
            print("connection attempt timed out. Retrying...")
        except sock.error as error: #if failed, print the error
            #print ("connection failed: ", error)
            pass
        except Exception as e:
            print("Aborting attempt to connect...")
    
    def send(self, data):
        try: #send the data through the com port. Must be a string or a ControlPacket type
            format_string = '=1c5f' 
            if len(data) == 6:
                dataFormat = (data[0].encode('utf-8'), data[1], data[2], data[3], data[4], data[5])
                mes = struct.pack(format_string, *dataFormat)
                self.conn.sendall(mes)
        except sock.error as e: #prints error otherwise
            print("error!: ", e)


    def receive(self):
        try:
            buf = b''
            while len(buf) < 80:
                part = self.conn.recv(80-len(buf))
                if part:
                    buf += part
            
            #self.streamData = self.conn.recv(80)  # 20 floats × 4 bytes = 80 bytes
            format = '=20f'
            mes = struct.unpack(format, buf)

            return list(mes)

        except sock.error as e:
            return None

    def close(self):
        self.connected = False
        self.conn.close()
        self.conn = None
            

