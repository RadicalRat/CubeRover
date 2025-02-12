import time as time
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


class TimePacket:
    def __init__(self,ImportedTimes):
        if (str(ImportedTimes).__len__() > 0):
            self.times = ImportedTimes
        else:
            self.times = str(time.time_ns())

    def addtime(self):
        self.times = self.times + ' ' + str(time.time_ns())

    def printTimes(self):
        tempstring = ""
        for i in self.times:
            if (i != ' '):
                tempstring += i
            else:
                print(tempstring)
                tempstring = ""
        print(tempstring)
    def printDelta(self):
        times = []
        tempstring = ""
        for i in self.times:
            if (i != ' '):
                tempstring += i
            else:
                times = np.append(times, float(tempstring))
                tempstring = ""
        times = np.append(times, float(tempstring))
        for i in range(np.size(times)):
            if (i != 0):
                print(times[i] - times[i-1])
            else:
                print(0)


# test1 = TimePacket("")
# test1.printTimes()

# time.sleep(1)

# test1.addtime()
# test1.printTimes()

# test2 = TimePacket(test1.times)
# time.sleep(1)
# test2.addtime()
# test2.printTimes()

# test2.printDelta()


