import PacketStruct as ps
import Networking as network
import time


serveraddress = ('127.0.0.1', 5555)

comm = network.NetworkClient(serveraddress)
comm.connect()


packet = ps.TimePacket("")
comm.send(packet.times)

# receive packet and convert to delta times
packet = ps.TimePacket(comm.recieve())
packet.addtime()
packet.printDelta()
