from pySerialTransfer import pySerialTransfer as txfer

'''The purpose of this class is to interface with the packet
layouts used on the teensy when sending data through the serial 
port with pySerialTransfer.'''

class packet:
    #initializes serial communication
    def __init__(self, port, baud):
        self.ser = txfer.SerialTransfer(port, baud=baud)
        self.ser.open()

    #Velocity control packet
    def V(self, vel1, vel2, delay):
        header = 'V'
        datasize = 0

        datasize = self.ser.tx_obj(header, start_pos=datasize, val_type_override='c')
        datasize = self.ser.tx_obj(vel1, start_pos=datasize,val_type_override='f')
        datasize = self.ser.tx_obj(vel2, start_pos=datasize,val_type_override='f')
        datasize = self.ser.tx_obj(delay, start_pos=datasize,val_type_override='f')

        self.ser.send(datasize)

    #Estop function
    def E(self):
        header = 'E'
        datasize = 0
        datasize = self.ser.tx_obj(header, start_pos=datasize, val_type_override='c')

        self.ser.send(datasize)

    #Radius Turning
    def T(self, angle, radius, speed):
        header = 'T'
        datasize = 0

        datasize = self.ser.tx_obj(header, start_pos=datasize, val_type_override='c')
        datasize = self.ser.tx_obj(angle, start_pos=datasize,val_type_override='f')
        datasize = self.ser.tx_obj(radius, start_pos=datasize,val_type_override='f')
        datasize = self.ser.tx_obj(speed, start_pos=datasize,val_type_override='f')

        self.ser.send(datasize)

    #Position
    def P(self, dist, vel):
        header = 'P'
        datasize = 0

        datasize = self.ser.tx_obj(header, start_pos=datasize, val_type_override='c')
        datasize = self.ser.tx_obj(dist, start_pos=datasize,val_type_override='f')
        datasize = self.ser.tx_obj(vel, start_pos=datasize,val_type_override='f')

        self.ser.send(datasize)

    #PID tuning
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

    #Recieves incoming serial communication
    def recv(self):
        rover_data = []
        if self.ser.available():
            index = int(0)
            num = 20

            for i in range(num):
                val = self.ser.rx_obj(obj_type='f', start_pos=index)
                rover_data.append(val)
                index += txfer.STRUCT_FORMAT_LENGTHS['f']
        if rover_data:
            return rover_data
        else:
            return []

        





    



        