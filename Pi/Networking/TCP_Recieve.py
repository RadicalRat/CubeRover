import subprocess
import GroundStation.Network.Networking as network
import time

serveraddress = ('0.0.0.0', 5555)

if __name__ == "__main__":

    comm = network.NetworkHost(serveraddress)
    comm.listenaccept()
    print(comm.recieve())
    time.sleep(0.00001)
    comm.send("Hello client!")
