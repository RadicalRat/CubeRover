import socket as sock
import PacketStruct as ps

if __name__ == "__main__":
    serveraddress = ('127.0.0.1', 5555)

    recieve = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
    print ("Socket created")
    recieve.bind(serveraddress)
    print ("Socket bound")
    recieve.listen(1)
    print ("Listening...")

    conn,adr = recieve.accept()
    print ("Connected!")
    print ("IP: ", adr)
    packet = ps.TimePacket(conn.recv(1024).decode())
    packet.printTimes()
    packet.addtime()
    conn.sendall(packet.times.encode())
