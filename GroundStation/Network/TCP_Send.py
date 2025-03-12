import GroundStation.Network.Networking as network
import struct
#Used to send controller inputs to pi over tcp wifi
#ID number feasibly not needed because order doesnt matter bc so much data

class sendTCP:
    def __init__(self, serveraddress):
        self.conn = network.NetworkClient(serveraddress)
        self.conn.connect()
    
    def sendTCP(self, data):
        mes = struct.pack('4l', *data)
        self.conn.send(mes)

    


