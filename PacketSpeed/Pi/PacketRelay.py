import subprocess
import Networking as network
from pySerialTransfer import pySerialTransfer as tx
import time
import struct
import numpy as np

serveraddress = ('127.0.0.1', 5555)
#COMPORT = 'COM7'

# def Decoder(data):
#     header = struct.unpack('1c',data[:1])[0].decode() # unpacks header
#     print(header)
#     match header: # uses header to unpack float data
#         case 'R':
#             data = struct.unpack('4f',data[1:])
#         case 'V':
#             data = struct.unpack('1f',data[1:])
#         case 'D':
#             data = struct.unpack('2f',data[1:])
    
#     dataset = np.array(data)
#     packet = (header[0], dataset) #stores the data in a set and returns
#     return packet

# def Encoder(data):
#     format_string = f'=1c{len(data)-1}f'
#     encodedData = struct.pack(format_string,data)
#     return encodedData




if __name__ == "__main__":

    GS = network.NetworkHost(serveraddress)
    #Teensy = tx.SerialTransfer(COMPORT,38400)
    GS.listenaccept()

    while True:
                    
            #Packet decoder
            recievedData = GS.recieve()
            decodedData = network.Decoder(recievedData)
            print(decodedData)
            #serial communication to teensy
            # datasize = 0
            # datasize = Teensy.tx_obj(decodedData[0], start_pos=datasize,val_type_override='c')
            # for i in decodedData[1]:
            #     datasize = Teensy.tx_obj(i,start_pos=datasize,val_type_override='f')
            # #Teensy.send()
            # print(decodedData)
            # print(datasize)

    #serial communication back from teensy


    #Packet encoder


    #Send packet

