import numpy as np

class ControlPacket:
    def __init__(self, ID):
        self.packet = np.array([0,0,0])
        self.ID = ID
    def encode(self):
        sep = ' '
        data = str(self.ID) + sep
        for i in self.packet:
            data += str(i) + sep
        return data
        


# Control1 = ControlPacket(1)


# print(Control1.encode())
