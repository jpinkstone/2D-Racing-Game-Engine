import pygame
import sys
import socket
import threading
import queue
import time
import select

class GameEngine():
    def __init__(self):
        try:
            self.game_state = FullGameState()
        except:
            print("Initilization of Game Engine Failed.")

    def add_player(self):
        player = PlayerGameState()
        self.game_state.add_player(player)

    def get_game_state(self):
        return self.game_state
    
    def update_game_state(self, game_state):
        self.game_state = game_state

    def get_keyboard_input(self):
        running = True
        while running:
            # Event handling
            for event in pygame.event.get():
                match event:
                    case pygame.QUIT:
                        running = False
                    case pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            self.game_state.main_player.accelerating = True
                        elif event.key == pygame.K_DOWN:
                            self.game_state.main_player.decelerating = True
                    case pygame.KEYUP:
                        if event.key == pygame.K_UP:
                            self.game_state.main_player.accelerating = False
                        elif event.key == pygame.K_DOWN:
                            self.game_state.main_player.decelerating = False

    def receive_game_state(self):
        # function of whatever networking class
        pass

    def send_game_state(self):
        # function of whatever networking class
        pass
    
    class NetworkingServer():
        def networking_thread(send, receive):
            print("Starting networking thread...")
            HOST = "127.0.0.1"
            PORT = 60217
        
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((HOST, PORT))
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
                        receive.put(message)
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
        
                        receive.put(message)
        
                if exit_flag:
                    print("Exiting...")
                    break
        
                for notified_socket in exception_sockets:
                    sockets_list.remove(notified_socket)
                
                if send.qsize() and len(sockets_list) > 1:
                    for client in range(1, len(sockets_list)):
                        sockets_list[client].sendall(send.get().encode())
                        
            s.close()
        
        def main_thread(send, receive):
            print("Starting main thread...")
            # Send data = send.put(string)
            # receive data = receive.get()
            while True:
                send.put("This is a test string to send. - server")
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
    
    class NetworkingClient():
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
    
    class Render():
        pass
