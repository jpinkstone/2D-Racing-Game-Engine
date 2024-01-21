import socket

HOST = "127.0.0.1"
MCAST_GRP = '224.1.1.1'
PORT = 60217

def server_connect():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)
    sock.sendto(str.encode(str(ip)), (MCAST_GRP, PORT))

def start_tcp():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        return s

def send_data(conn, data):
    conn.sendall(data)

def receive_data(conn):
    return conn.recv(1024)