import socket as sock
import struct

        
class NetworkHost:
    def __init__(self,serveraddress):
        #stores server address, and binds it to the socket
        self.address = serveraddress
        self.streamData = ()
        self.conn = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        self.conn.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1) #reuse socket
        self.connected = False
        try:
            self.conn.bind(self.address)
        except sock.error as e:
            print(f"Failed to bind to address {self.address}: {e}")
            print("Trying to close any existing connections...")
            self.close()
            raise e


    def listenaccept(self):
        self.conn.listen(1)
        print("Listening...")
        self.client,self.clientadr = self.conn.accept()
        print("Client Connected:", self.clientadr)
        self.connected=True
    
    def recieve(self):
        try:
            self.streamData = self.client.recv(1024)
            if not self.streamData:
                raise ConnectionResetError("Client Disconnected")
        except (sock.error, ConnectionResetError) as e:
            print("error!", e)
            self.close()
            raise e

    def send(self, data):
        try: #send the data through the com port. Must be a string or a ControlPacket type
            format_string = '=20f'

            if len(data) == 20: #this is the correct length of input data
                data_form = tuple(data)
                mes = struct.pack(format_string, *data_form)
                self.client.sendall(mes)


            else:
                print("where is this data coming from")

        except sock.error as e: #prints error otherwise
            print("error!: ", e)

    def decodeGround(self): #decode incoming data from computer to Pi
        #format_string = f'={int((len(self.streamData) - len(self.streamData) % 4) /4)}f'
        format_string = '=1c5f'
        try:
            mes = struct.unpack(format_string, self.streamData)
            data = [mes[0].decode(), mes[1], mes[2], mes[3], mes[4], mes[5]]
            return data
        except:
            return None
    def close_client(self):
        try:
            self.client.close()
        except:
            pass
        self.connected = False
    
    def close(self):
        try:
            self.connected = False
            self.client.close()
            self.conn.close()

        except:
            pass
