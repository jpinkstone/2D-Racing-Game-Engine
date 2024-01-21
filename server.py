import socket
import struct

HOST = "127.0.0.1"
MCAST_GRP = '224.1.1.1'
PORT = 60217

def get_ip():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', PORT))
    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    return (sock.recv(10240).decode())

def start_tcp():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        return conn

def send_data(conn, data):
    with conn:
        conn.sendall(data)

def receive_data(conn):
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            return data

print(get_ip())