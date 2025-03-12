import socket as sock
import struct
import time
import GroundStation.Network.Networking as network
import numpy as np



def Encoder(data):
    format_string = f'=1c{len(data)-1}f'
    return struct.pack(format_string,*data) #bytes

serveraddress = ('127.0.0.1', 5555)

conn = network.NetworkClient(serveraddress)
conn.connect()

# num = (b'V', 0,12,54,6235,12,512)


while True:
    header = input("Input Header: ") #ID num
    length = int(input("Input length as a int: "))
    data = (header[0].encode(),)
    for i in range(length):
        data = data + (float(input(f'Input value #{i+1}: ')),)
    print(data)
    conn.send(Encoder(data))