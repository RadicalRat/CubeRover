import socket as sock
import struct
import time
import Networking as network
from pySerialTransfer import pySerialTransfer as tx
import serial as ser

def Decoder(data):
    format_string = f'=1c{int((len(data) - len(data)%4)/4)}f'
    return struct.unpack(format_string,data)


COMPORT = 'COM7'
serveraddress = ('127.0.0.1', 5555)

serial = tx.SerialTransfer(COMPORT,38400)
serial2 = ser.Serial(baudrate=38400,timeout=100)
serial2.port = COMPORT
try:
    serial.open()
except:
    time.sleep(3)
    serial.open()

conn = network.NetworkHost(serveraddress)
conn.listenaccept()

while True:
    serial.open()
    recieved = conn.recieve()
    print(recieved)
    print(Decoder(recieved))
    decoded = Decoder(recieved)
    # send serial commands to teensy
    datasize = 0
    datasize = serial.tx_obj(decoded[0].decode(),start_pos=datasize,val_type_override='c')
    dataLen = int((len(recieved) - len(recieved)%4)/4)
    for i in range(dataLen):
        datasize = serial.tx_obj(decoded[i+1],start_pos=datasize,val_type_override='f')
    serial.send(datasize)
    serial.close()
    serial2.open()
    out = serial2.readline()
    while out:
        print(f"Received: {out.decode().strip()}")
        out = serial2.readline()
        print("going")
    serial2.close()