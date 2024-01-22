import socket
import threading
import queue
import time

# MCAST_GRP = '224.1.1.1'

# def server_connect():
#     hostname = socket.gethostname()
#     ip = socket.gethostbyname(hostname)
#     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
#     sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)
#     sock.sendto(str.encode(str(ip)), (MCAST_GRP, PORT))

def networking_thread(send, receive):
    print("Starting networking thread...")
    HOST = "127.0.0.1"
    PORT = 60217

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    while True:
        if send.qsize():
            s.sendall(send.get().encode())
        try:
            message = s.recv(1024).decode()
        except:
            print("Exiting")
            break
        if not message or message == "exit":
            print("Exiting")
            break
        else:
            receive.put(message)
    s.close()

def main_thread(send, receive):
    print("Starting main thread...")
    while True:
        send.put("This is a test string to send. - client")
        time.sleep(1)
        if receive.qsize():
            print(receive.get())

def startup():
    send = queue.Queue()
    receive = queue.Queue()
    netwokring = threading.Thread(target=networking_thread, args=(send, receive))
    main = threading.Thread(target=main_thread, args=(send, receive))
    netwokring.start()
    main.start()
    netwokring.join()
    main.join()
    print("Both threads have rejoined")


if __name__ == '__main__':
    startup()
