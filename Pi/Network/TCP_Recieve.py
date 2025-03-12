import struct
import Network.Networking as network
import time

class receiveTCP:
    def __init__(self, serveraddress):
        self.conn = network.NetworkHost(serveraddress)
        
