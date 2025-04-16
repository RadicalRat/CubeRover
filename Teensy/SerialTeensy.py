from pySerialTransfer import pySerialTransfer as tx
import time
import struct

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
    



    while True:
        ID = 'V'
        datasize = 0
        datasize = serial.tx_obj(ID,start_pos=datasize,val_type_override='c')
        val = int(input("Enter Val: "))
        datasize = serial.tx_obj(val,start_pos=datasize,val_type_override="f")
        val = int(input("Enter Val: "))
        datasize = serial.tx_obj(val,start_pos=datasize,val_type_override="f")
        # print(val)
        # for i in range(2):
        #     datasize = serial.tx_obj(val,start_pos=datasize,val_type_override="f")
        #     print(serial.txBuff.count(val))
        serial.send(datasize)
        print(datasize)
    
    