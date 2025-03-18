import PacketStruct as ps
import Networking as network
import time

serveraddress = ('127.0.0.1', 5555)

if __name__ == "__main__":
    
    comm = network.NetworkClient(serveraddress)
    comm.connect()
    data = (b'R',128,0,56,12)
    encodedData = network.Encoder(data)

    comm.send(encodedData)
    print("sent")
    # receive packet and convert to delta times
    
