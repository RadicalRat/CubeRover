import Network.Networking as network
import struct
#Used to send controller inputs to pi over tcp wifi

class sendTCP:
    def __init__(self, serveraddress):
        self.testing = False
        self.conn = network.NetworkClient(serveraddress)
        self.conn.connect()
    
    def send(self, data):
        format_string = '=1c5f'

        if self.testing: #testing mode header
            header = 'T'.encode('utf-8')

        else: #controller mode header
            header = 'C'.encode('utf-8')

        if len(data) == 5: #this is the correct length of input data
            dataFormat = (header, data[0], data[1], data[2], data[3], data[4], data[5])
            print(dataFormat)
            mes = struct.pack(format_string, *dataFormat)
            self.conn.send(mes)


        else:
            print("where is this data coming from")
