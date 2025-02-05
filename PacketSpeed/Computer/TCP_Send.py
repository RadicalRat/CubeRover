import socket as sock
import PacketStruct as ps
import Networking as network


serveraddress = ('127.0.0.1', 5555)

transfer = network.Network(serveraddress)
transfer.connect()
packet = ps.ControlPacket(int(input("Enter header: ")))
transfer.send(packet.encode())


# transfer = sock.socket(sock.AF_INET, sock.SOCK_STREAM)

# #establish connection with host
# transfer.connect(serveraddress)

# while True:
#     transmission = str(input("Enter a string of data"))
#     transfer.send(transmission.encode())

