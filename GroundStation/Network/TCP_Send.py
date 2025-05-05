import Network.Networking as network
import struct
#Used to send controller inputs to pi over tcp wifi

class sendTCP:
    def __init__(self, serveraddress):
        self.conn = network.NetworkClient(serveraddress)
        self.conn.connect()
        self.streamData = ()
    
    def send(self, data):
        format_string = '=1c5f'

        if len(data) == 6: #this is the correct length of input data
            dataFormat = (data[0].encode('utf-8'), data[1], data[2], data[3], data[4], data[5])
            print(dataFormat)
            mes = struct.pack(format_string, *dataFormat)
            self.conn.send(mes)

        else:
            print("where is this data coming from")

    def receive(self):
        try:
            self.conn.recieve()
            return self.conn.decodePi()
        except Exception as e:
            print("error!", e)
            return None

