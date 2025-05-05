from pySerialTransfer import pySerialTransfer as pySer


class packet:
    def __init__(self, port, baud):
        self.ser = pySer.SerialTransfer(port, baud=baud)
        self.ser.open()

    # def recv(self):
    #     if self.ser.available():
    #         status = self.ser.status

    #         if status == pySer.CRC_OK:
    #             #first is the length
    #             length = self.ser.rx_buff[0]
    #             data = list(self.ser.rx_buff[1:1+length])


    def V(self, vel1, vel2, delay):
        header = 'V'
        datasize = 0

        datasize = self.ser.tx_obj(header, start_pos=datasize, val_type_override='c')
        datasize = self.ser.tx_obj(vel1, start_pos=datasize,val_type_override='f')
        datasize = self.ser.tx_obj(vel2, start_pos=datasize,val_type_override='f')
        datasize = self.ser.tx_obj(delay, start_pos=datasize,val_type_override='f')

        self.ser.send(datasize)

    def E(self):
        header = 'E'
        datasize = 0
        datasize = self.ser.tx_obj(header, start_pos=datasize, val_type_override='c')

        self.ser.send(datasize)

    def T(self, angle, radius, speed):
        header = 'T'
        datasize = 0

        datasize = self.ser.tx_obj(header, start_pos=datasize, val_type_override='c')
        datasize = self.ser.tx_obj(angle, start_pos=datasize,val_type_override='f')
        datasize = self.ser.tx_obj(radius, start_pos=datasize,val_type_override='f')
        datasize = self.ser.tx_obj(speed, start_pos=datasize,val_type_override='f')

        self.ser.send(datasize)

    def P(self, dist, vel):
        header = 'P'
        datasize = 0

        datasize = self.ser.tx_obj(header, start_pos=datasize, val_type_override='c')
        datasize = self.ser.tx_obj(dist, start_pos=datasize,val_type_override='f')
        datasize = self.ser.tx_obj(vel, start_pos=datasize,val_type_override='f')

        self.ser.send(datasize)

    def C(self, pid, start):
        header = 'C'
        address = start

        for i in pid:
            if i != None:

                datasize = 0

                datasize = self.ser.tx_obj(header, start_pos=datasize, val_type_override='c')
                datasize = self.ser.tx_obj(address, start_pos=datasize,val_type_override='f')
                datasize = self.ser.tx_obj(i, start_pos=datasize,val_type_override='f')
                self.ser.send(datasize)

            address += 4

    def recv(self):
        rover_data = []
        if self.ser.available():
            print("avail")
            if self.ser.status == 0:
                print("in")
                index = 0
                num = 20

                for i in range(num):
                    val = self.ser.rx_obj(obj_type='f', start_pos=index)
                    rover_data.append(val)
                    index += pySer.STRUCT_FORMAT_LENGTHS['f']
        if rover_data:
            return rover_data
        else:
            return []

        





    



        