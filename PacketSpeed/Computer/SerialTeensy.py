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
        ID = 'V'
        datasize = 0
        datasize = serial.tx_obj(ID,start_pos=datasize,val_type_override='c')
        val = int(input("Enter Val: "))
        for i in range(1):
            datasize = serial.tx_obj(val,start_pos=datasize,val_type_override="i")
            datasize = serial.tx_obj(val,start_pos=datasize,val_type_override="i")
        serial.send(datasize)
        print(datasize)
    
    