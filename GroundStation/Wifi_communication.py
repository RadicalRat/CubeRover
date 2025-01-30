#using UDP protocol because its fast and doesn't have to be super reliable

import socket

pi_ip = "10.42.0.1"
port = 65432

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send_data():
    message = "5"
    sock.sendto(message.encode(), (pi_ip, port))

send_data()
