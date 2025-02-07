import PacketStruct as ps
import Networking as network
import time


serveraddress = ('127.0.0.1', 5555)

transfer = network.Network(serveraddress)
transfer.connect()



packet = ps.TimePacket("")
transfer.send(packet.times)

# receive packet and convert to delta times
packet = ps.TimePacket(transfer.conn.recv(1024).decode())
time.sleep(0.00000000001)
packet.addtime()
packet.printDelta()



# transfer = sock.socket(sock.AF_INET, sock.SOCK_STREAM)

# #establish connection with host
# transfer.connect(serveraddress)

# while True:
#     transmission = str(input("Enter a string of data"))
#     transfer.send(transmission.encode())

