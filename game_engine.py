import socket
import threading
import queue
import select
import pygame
import math
import sys
import os
import datetime

EVENT_ACCELF = "accelF"
EVENT_ACCELB = "accelB"
EVENT_DECELF = "decelF"
EVENT_DECELB = "decelB"
EVENT_REDUCE_SPEED = "reduce"
EVENT_LEFT = "left"
EVENT_RIGHT = "right"
EVENT_RESTART = "restart"
EVENT_ENTER = "enter"
EVENT_QUIT = "quit"
EVENT_COLLISION = "collision"

ACCELERATION_FACTOR = 1.5
ROTATION_INCREMENT = 10

from game_state import *

class GameEngine():
    def __init__(self, state):
        try:
            self.screen = pygame.display.set_mode(state.dimensions)
            pygame.display.set_caption(state.title)
            self.clock = pygame.time.Clock()
            self.assets = None
            print("Game initialized")
        except:
            print("Initilization of Game Engine Failed.")

    def render(self):
        pygame.display.update()

    def screenFill(self, color):
        self.screen.fill(color)

    def clear(self):
        self.screenFill((0, 0, 0))

    def addText(self, x_dim, y_dim, font, size, text):
        font = pygame.font.Font(font, size)
        text = font.render(text, True, (0, 0, 0), None)
        rect = text.get_rect()
        rect.center = (x_dim, y_dim)
        self.screen.blit(text, rect)
    
    # Need to add argument for image mask for collisions
    def addMap(self, map, map_mask, dimensions):
        scaled = pygame.transform.scale(self.assets[map], dimensions)
        self.screen.blit(scaled, (0, 0))

        scaled_mask = pygame.transform.scale(self.assets[map_mask], dimensions)
        mask = pygame.mask.from_surface(scaled_mask)
        return mask

    # Need to add argument for image mask for collisions
    def placePlayer(self, player, dimensions):
        img_rect = self.assets["race_car0.png"].get_rect()
        rotated = pygame.transform.rotate(self.assets["race_car0.png"], player.player_angle)
        rot_rect = img_rect.copy()
        rot_rect.center = rotated.get_rect().center
        rotated = rotated.subsurface(rot_rect).copy()
        scaled = pygame.transform.scale(rotated, dimensions)
        self.screen.blit(scaled, (player.player_x, player.player_y))

        mask = pygame.mask.from_surface(scaled)
        return mask

    def getCollisions(self, mask1, obj1, mask2, state):
        if mask1.overlap(mask2, (obj1.player_x, obj1.player_y)):
            self.handle_actions(state, EVENT_COLLISION)

    def loadAssets(self, assets):
        surfaces = {}
        for asset in assets:
            surfaces[asset] = pygame.image.load(os.path.join("assets", asset)).convert_alpha()
        self.assets = surfaces

    def handle_actions(self, state, actions):
        if EVENT_ACCELF in actions:
            self.accelerate(state, ACCELERATION_FACTOR)
        if EVENT_ACCELB in actions:
            self.accelerate(state, -ACCELERATION_FACTOR)
        if EVENT_REDUCE_SPEED in actions:
            self.decelerate(state)
        if EVENT_LEFT in actions:
            self.rotate(state, -ROTATION_INCREMENT)
        if EVENT_RIGHT in actions:
            self.rotate(state, ROTATION_INCREMENT)
        if EVENT_COLLISION in actions:
            self.bounce(state)
        if EVENT_QUIT in actions:
            self.quit(state)

    def accelerate(self, state, direction):
        temp_player = state.players[0]

        # Adjusting speed
        temp_player.player_speed += temp_player.acceleration
        temp_player.player_speed = min(temp_player.player_speed, temp_player.player_max_speed)

        # Calculate velocity
        temp_player.player_velocity[0] = direction * temp_player.player_speed * pygame.math.Vector2(1, 0).rotate(-temp_player.player_angle).x
        temp_player.player_velocity[1] = direction * temp_player.player_speed * pygame.math.Vector2(1, 0).rotate(-temp_player.player_angle).y
        
        # Change coordinates
        temp_player.player_x += temp_player.player_velocity[0]
        temp_player.player_y += temp_player.player_velocity[1]

        state.players[0] = temp_player

    def decelerate(self, state):
        temp_player = state.players[0]
    
        deceleration = temp_player.acceleration / 2
        
        temp_player.player_velocity[0] -= deceleration * (1 if temp_player.player_velocity[0] > 0 else -1)
        temp_player.player_velocity[1] -= deceleration * (1 if temp_player.player_velocity[1] > 0 else -1)
        
        temp_player.player_velocity[0] = max(temp_player.player_velocity[0], -temp_player.player_max_speed)
        temp_player.player_velocity[1] = max(temp_player.player_velocity[1], -temp_player.player_max_speed)
        
        temp_player.player_x += temp_player.player_velocity[0]
        temp_player.player_y += temp_player.player_velocity[1]

        state.players[0] = temp_player

    def rotate(self, state, angle_increment):
        temp_player = state.players[0]
        temp_player.player_angle -= angle_increment
        state.players[0] = temp_player
    
    def bounce(self, state):
        temp_player = state.players[0]

        temp_player.player_velocity[0] = -temp_player.player_velocity[0]
        temp_player.player_velocity[1] = -temp_player.player_velocity[1]

        state.players[0] = temp_player

    def quit(self, state):
        state.cycle = "quit"

    def addPlayer(self, state, player):
        state.players.append(player)
    
    def setGameTime(self, state, seconds):
        state.gameTime = seconds

    def setLastTime(self, state, time):
        state.lastTime = time
    
    def decreaseGameTime(self, state, num):
        state.gameTime -= num
    
class PlayerAI(GameEngine):
    def __init__(self, max_vel, rotation_vel, path=[]):
        try:
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
            self.type = type
            self.host = ip
            self.port = port
            self.sendQ = queue.Queue()
            self.receiveQ = queue.Queue()
            self.status = "running"
        except:
            print("Initilization of networking Failed.")

    # Start networking and main loop threads
    def start(self, gameLoop):
        if self.type == "server":
            network = threading.Thread(target=self.networkingThreadServer, args=())
        else:
            network = threading.Thread(target=self.networkingThreadClient, args=())
        main = threading.Thread(target=gameLoop, args=(self.send, self.receive))
        network.start()
        main.start()
        main.join()
        sys.exit()

    def end(self):
        self.status = "stopped"
    
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
            if self.status == "stopped":
                print("Exiting")
                break
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
            if self.status == "stopped":
                exit_flag = True
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

class audio(GameEngine):
    def startMusic():
        pass

class physics(GameEngine):
    pass
