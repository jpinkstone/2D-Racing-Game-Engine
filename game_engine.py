import socket
import threading
import queue
import select
import pygame
import math

class GameEngine():
    def __init__(self, state):
        try:
            self.state = state
            pygame.init()
            self.screen = pygame.display.set_mode(state.screen)
            self.screen.fill((255, 255, 255))
            pygame.display.set_caption(state.title)
            self.clock = pygame.time.Clock()
        except:
            print("Initilization of Game Engine Failed.")

    class EngineActions():
        def __init__(self):
            try:
                self.state = self.state
            except:
                print("Initilization of EngineActions Failed.")

        def addPlayer(self, player):
            self.state.players.append(player)
        
        def startGame(self):
            pass
    
    class PlayerAI():
        def __init__(self, max_vel, rotation_vel, path=[]):
            try:
                self.state = self.state
                super().__init__(max_vel, rotation_vel)
                self.path = path
                self.current_point = 0
                self.vel = max_vel
            except:
                print("Initilization of PlayerAI Failed.")

        def draw_points(self, win):
            for point in self.path:
                pygame.draw.circle(win, (255, 0, 0), point, 5)

        def draw(self, win):
            super().draw(win)
            # self.draw_points(win)

        def calculate_angle(self):
            target_x, target_y = self.path[self.current_point]
            x_diff = target_x - self.x
            y_diff = target_y - self.y
            if y_diff == 0:
                desired_radian_angle = math.pi / 2
            else:
                desired_radian_angle = math.atan(x_diff / y_diff)

            if target_y > self.y:
                desired_radian_angle += math.pi

            difference_in_angle = self.angle - math.degrees(desired_radian_angle)
            if difference_in_angle >= 180:
                difference_in_angle -= 360

            if difference_in_angle > 0:
                self.angle -= min(self.rotation_vel, abs(difference_in_angle))
            else:
                self.angle += min(self.rotation_vel, abs(difference_in_angle))

        def update_path_point(self):
            target = self.path[self.current_point]
            rect = pygame.Rect(
                self.x, self.y, self.img.get_width(), self.img.get_height())
            if rect.collidepoint(*target):
                self.current_point += 1
        def move(self):
            if self.current_point >= len(self.path):
                return

            self.calculate_angle()
            self.update_path_point()
            super().move()
    
    class networking():
        # Initialize networking variables, connection type, and data queues
        def __init__(self, type, ip, port):
            try:
                self.state = self.state
                self.type = type
                self.host = ip
                self.port = port
                self.sendQ = queue.Queue()
                self.receiveQ = queue.Queue()
            except:
                print("Initilization of networking Failed.")
    
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

    class GameActions():
        def __init__(self, action):
            try:
                self.state = self.state
                if action == "accelF": self.accelF()
                elif action == "accelB": self.accelB()
                elif action == "decelF": self.decelF()
                elif action == "decelB" : self.decelB()
                elif action == "left": self.left()
                elif action == "right": self.right()
                elif action == "quit": self.quit()
            except:
                print("Initilization of GameActions Failed.")

        def accelF(self):
            pass

        def accelB(self):
            pass

        def decelF(self):
            pass

        def decelB(self):
            pass

        def left(self):
            pass

        def right(self):
            pass

        def quit(self):
            self.state.cycle = "quit"

    class render():
        pygame.display.flip()
    
    class screen():
        def __init__(self):
            try:
                self.state = self.state
                self.screen = self.screen
            except:
                print("Initilization of screen Failed.")

        def fill(self, color):
            self.screen.fill(color)

        def clear(self):
            pass

        def addText(self):
            pass

        def addMap(self):
            pass

    class audio():
        def startMusic():
            pass

    class physics():
        pass
