from pySerialTransfer import pySerialTransfer as tx
import time
import struct
import random

COMPORT = 'COM7'

def Encoder(data):
    format_string = f'=1c{len(data)-1}f'
    encodedData = struct.pack(format_string,data)
    return encodedData


if __name__ == "__main__":
    serial = tx.SerialTransfer(COMPORT,38400)
    try:
        serial.open()
    except:
        time.sleep(3)
        serial.open()
    


    ID = 'V'
    # while True:
        # for i in range(1,1000):
        #     datasize = 0
        #     datasize = serial.tx_obj(ID,start_pos=datasize,val_type_override='c')
        #     datasize = serial.tx_obj(i,start_pos=datasize,val_type_override="f")
        #     datasize = serial.tx_obj(i,start_pos=datasize,val_type_override="f")
        #     serial.send(datasize)
        #     time.sleep(0.01)
        # for i in range(1000,1):
        #     datasize = 0
        #     datasize = serial.tx_obj(ID,start_pos=datasize,val_type_override='c')
        #     datasize = serial.tx_obj(i,start_pos=datasize,val_type_override="f")
        #     datasize = serial.tx_obj(i,start_pos=datasize,val_type_override="f")
        #     serial.send(datasize)
        #     time.sleep(0.01)
    for i in range(5):
        datasize = 0
        randval =  random.randint(500,3000)
        datasize = serial.tx_obj(ID,start_pos=datasize,val_type_override='c')
        datasize = serial.tx_obj(1000,start_pos=datasize,val_type_override="f")
        datasize = serial.tx_obj(0,start_pos=datasize,val_type_override="f")
        datasize = serial.tx_obj(1000,start_pos=datasize,val_type_override="f")
        serial.send(datasize)
        time.sleep(0.05)
    
    