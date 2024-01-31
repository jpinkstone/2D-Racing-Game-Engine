import pygame
import sys
import socket
import threading
import queue
import time
import select
from game_state import *

class GameEngine():
    def __init__(self):
        try:
            self.game_state = FullGameState()
            self.net = self.networking()
        except:
            print("Initilization of Game Engine Failed.")

    def add_player(self):
        player = PlayerGameState()
        self.game_state.add_player(player)

    def get_game_state(self):
        return self.game_state
    
    def update_game_state(self, game_state):
        self.game_state = game_state

    def receive_game_state(self):
        # function of whatever networking class
        pass

    def send_game_state(self):
        # function of whatever networking class
        pass
    
    class networking():
        # Initialize networking variables, connection type, and data queues
        def __init__(self, type, ip, port):
            self.type = type
            self.host = ip
            self.port = port
            self.sendQ = queue.Queue()
            self.receiveQ = queue.Queue()
    
        # Start networking and main loop threads
        def start(self, gameLoop):
            if self.type == "server":
                netwokring = threading.Thread(target=self.networkingThreadServer, args=())
            else:
                netwokring = threading.Thread(target=self.networkingThreadClient, args=())
            main = threading.Thread(target=gameLoop, args=(self.send, self.receive))
            netwokring.start()
            main.start()
            netwokring.join()
            main.join()
            print("Both threads have rejoined")
        
        # Send data to all connected devices
        def send(self, data):
            self.sendQ.put(data)
    
        # Receive data from all connected devices
        def receive(self):
            if self.receiveQ.qsize():
                return self.receiveQ.get()
        
        # Handle networking for the client devices
        def networkingThreadClient(self):
            print("Starting client networking thread...")
    
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.host, self.port))
    
            while True:
                if self.sendQ.qsize():
                    s.sendall(self.sendQ.get().encode())
                try:
                    message = s.recv(1024).decode()
                except:
                    print("Exiting")
                    break
                if not message or message == "exit":
                    print("Exiting")
                    break
                else:
                    self.receiveQ.put(message)
            s.close()
        
        # Handle networking for the server device
        def networkingThreadServer(self):
            print("Starting server networking thread...")
    
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.host, self.port))
            s.listen()
    
            sockets_list = [s]
            exit_flag = False
    
            while True:
                read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list, 0)
                for notified_socket in read_sockets:
                    # New connection
                    if notified_socket == s:
                        client_socket, client_address = s.accept()
                        try:
                            message = client_socket.recv(1024).decode()
                        except:
                            exit_flag = True
                            break
                        if message is False:
                            continue
                        elif message == "exit":
                            exit_flag = True
                            break
    
                        sockets_list.append(client_socket)
                        self.receiveQ.put(message)
                    # Existing client is sending a message
                    else:
                        try:
                            message = notified_socket.recv(1024).decode()
                        except:
                            exit_flag = True
                            break
    
                        if message is False:
                            sockets_list.remove(notified_socket)
                            continue
                        elif message == "exit":
                            exit_flag = True
                            break
    
                        self.receiveQ.put(message)
    
                if exit_flag:
                    print("Exiting...")
                    break
    
                for notified_socket in exception_sockets:
                    sockets_list.remove(notified_socket)
                
                if self.sendQ.qsize() and len(sockets_list) > 1:
                    for client in range(1, len(sockets_list)):
                        sockets_list[client].sendall(self.sendQ.get().encode())
                        
            s.close()
    
    class Render():
        pass
