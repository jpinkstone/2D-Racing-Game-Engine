import socket
import threading
import queue
import time
import select

# MCAST_GRP = '224.1.1.1'

# def server_connect():
#     hostname = socket.gethostname()
#     ip = socket.gethostbyname(hostname)
#     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
#     sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)
#     sock.sendto(str.encode(str(ip)), (MCAST_GRP, PORT))

def networking_thread(q):
    HOST = "127.0.0.1"
    PORT = 60217

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    while True:
        if q.qsize():
            s.sendall(q.get().encode())
        data = s.recv(1024).decode()
        if not data or data == "exit": 
            break
        else:
            print(data)
    s.close()

def main_thread(q):
    string = "This is a test string to send. - client"
    for i in range(0, 100000):
        q.put(string + " : " + str(i))
        # time.sleep(1)

def startup():
    q = queue.Queue()
    netwokring = threading.Thread(target=networking_thread, args=(q, ))
    main = threading.Thread(target=main_thread, args=(q, ))
    netwokring.start()
    main.start()
    netwokring.join()
    main.join()


if __name__ == '__main__':
    startup()
