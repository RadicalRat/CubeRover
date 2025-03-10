from UDP_Receiver import receive_UDP

server = receive_UDP()

try:
    while True:
        data = server.receive_data()
        print(data)

except KeyboardInterrupt:
    server.close()