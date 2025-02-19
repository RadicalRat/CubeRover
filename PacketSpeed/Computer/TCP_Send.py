import PacketStruct as ps
import Networking as network
import time

serveraddress = ('127.0.0.1', 5555)

if __name__ == "__main__":
    
    comm = network.NetworkClient(serveraddress)
    comm.connect()
    comm.send("Hi server")
    # receive packet and convert to delta times
    print(comm.recieve())
