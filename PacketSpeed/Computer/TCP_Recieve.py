import socket as sock
import PacketStruct as ps
import Networking as network
import time

serveraddress = ('127.0.0.1', 5555)

if __name__ == "__main__":

    recieve = network.NetworkHost(serveraddress)
    recieve.listenaccept()
    packet = ps.TimePacket(recieve.recieve())
    packet.printTimes()
    time.sleep(0.00000000001)
    packet.addtime()
    recieve.send(packet.times)
