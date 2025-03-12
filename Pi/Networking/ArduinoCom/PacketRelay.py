import subprocess
import GroundStation.Network.Networking as network
import pySerialTransfer as tx
import time
import struct
import numpy as np

serveraddress = ('10.42.0.1', 5555)
COMPORT = 'COM7'

def Decoder(data):
    header = struct.unpack('1c',data[:1])[0].decode()
    print(header)
    match header:
        case 'R':
            data = struct.unpack('4f',data[1:])
        case 'V':
            data = struct.unpack('1f',data[1:])
        case 'D':
            data = struct.unpack('2f',data[1:])
    
    dataset = np.array(data)
    packet = (header[0], dataset)
    return packet



if __name__ == "__main__":
    GS = network.NetworkHost(serveraddress)
    Teensy = tx.SerialTransfer(COMPORT,38400)
    GS.listenaccept()

    #Packet decoder

    recievedData = GS.recieve()
    decodedData = Decoder(recievedData)
    

    #serial communication to teensy
    

    #serial communication back from teensy


    #Packet encoder


    #Send packet

