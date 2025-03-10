import socket as sock
import PacketStruct as ps
import Networking as network
import time

serveraddress = ('127.0.0.1', 5555)

if __name__ == "__main__":

    comm = network.NetworkHost(serveraddress)
    comm.listenaccept()
    print(comm.recieve())
    time.sleep(0.00001)
    comm.send("Hello client!")
