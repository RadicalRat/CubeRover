from pySerialTransfer import pySerialTransfer as tx
import time

COMPORT = 'COM7'



if __name__ == "__main__":
    serial = tx.SerialTransfer(COMPORT)
    serial.open()
    time.sleep(5)
    
    datasize = 0
    datasize = serial.tx_obj('A')
    data = [0,0,0,0]
    for i in range(4):
        data[i] = int(input("Enter val:"))
    datasize = serial.tx_obj(data)
    serial.send(datasize)

    
    