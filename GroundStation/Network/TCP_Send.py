import Network.Networking as network
import struct
#Used to send controller inputs to pi over tcp wifi

class sendTCP:
    def __init__(self, serveraddress):
        self.testing = False
        self.conn = network.NetworkClient(serveraddress)
        self.conn.connect()
    
    def send(self, data):
        format_string = '=1c3f'

        if self.testing: #testing mode header
            header = 'T'

        else: #controller mode header
            header = 'C'

        if len(data) == 4: #this is the correct length of input data
            mes = (header.encode(), data[0], data[1], data[2], data[3])
            mes = struct.pack(format_string, *data)
            self.conn.send(mes)

        else:
            print("where is this data coming from")

    


