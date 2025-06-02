from pySerialTransfer import pySerialTransfer as tx
import time
import numpy as np
import sys

COMPORT = 'COM9'

serial = tx.SerialTransfer(COMPORT,38400)
serial.open()
data = ()

time.sleep(1)
recSize = 0

data = np.empty(22,dtype=float)

while True:
    flag = 0
    while not serial.available():
        flag = 1
        continue
    if flag == 1:
        continue
    # print("data: ")
    # print(serial.bytes_read)
    # serial.available()
    # data = serial.rx_obj(obj_type=type(data),obj_byte_size=sys.getsizeof(data), list_format='f')
    # print(data)
    # print('\n')
    float_list = []
    index = 0
    print(serial.rx_buff)
    print(type(serial.rx_buff))
    for i in range(23):
        print(serial.rx_obj(obj_type='f', start_pos=index))
        # float_list.append(val)
        # print(i)
        index += 4
    time.sleep(0.5)