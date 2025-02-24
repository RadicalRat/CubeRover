from pySerialTransfer import pySerialTransfer as tx
import time

COMPORT = 'COM7'



if __name__ == "__main__":
    serial = tx.SerialTransfer(COMPORT,38400)
    try:
        serial.open()
    except:
        time.sleep(3)
        serial.open()
    
    while True:
        ID = 'D'
        datasize = 0
        datasize = serial.tx_obj(ID,start_pos=datasize,val_type_override='c')
        datasize = serial.tx_obj(1000,start_pos=datasize,val_type_override="i")
        val = int(input("Enter Val: "))
        for i in range(1):
            datasize = serial.tx_obj(val,start_pos=datasize,val_type_override="i")
        serial.send(datasize)
        print(datasize)
    
    