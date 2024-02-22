import socket
import threading
import queue
import select
import math
import sys
import datetime
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from pygame import mixer

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

mixer.init()
accel_sound = pygame.mixer.Sound(os.path.join("assets", "Recording.wav"))
accel_sound.set_volume(0.2)

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

    def addText(self, x_dim, y_dim, font, size, color, text):
        font = pygame.font.Font(font, size)
        text = font.render(text, True, color, None)
        rect = text.get_rect()
        rect.center = (x_dim, y_dim)
        self.screen.blit(text, rect)
    
    def addMap(self, map, map_mask, dimensions):
        scaled = pygame.transform.scale(self.assets[map], dimensions)
        self.screen.blit(scaled, (0, 0))

        scaled_mask = pygame.transform.scale(self.assets[map_mask], dimensions)
        mask = pygame.mask.from_surface(scaled_mask)
        return mask
    
    def addSplash(self, splash, dimensions):
        scaled = pygame.transform.scale(self.assets[splash], dimensions)
        self.screen.blit(scaled, (0, 0))

    def placePlayer(self, player, dimensions):
        img_rect = self.assets["race_car2.png"].get_rect()
        rotated = pygame.transform.rotate(self.assets["race_car2.png"], player.player_angle)
        rot_rect = img_rect.copy()
        rot_rect.center = rotated.get_rect().center
        rotated = rotated.subsurface(rot_rect).copy()
        scaled = pygame.transform.scale(rotated, dimensions)
        self.screen.blit(scaled, (player.player_x, player.player_y))

        mask = pygame.mask.from_surface(scaled)
        return mask

    def getCollisions(self, mask1, obj1, mask2, state):
        if mask1.overlap(mask2, (obj1.player_x, obj1.player_y)):
            return True
        else:
            return False

    def loadAssets(self, assets):
        surfaces = {}
        for asset in assets:
            surfaces[asset] = pygame.image.load(os.path.join("assets", asset)).convert_alpha()
        self.assets = surfaces

    def handle_actions(self, state, actions):
        if EVENT_ACCELF in actions:
            self.forward(state)
        if EVENT_ACCELB in actions:
            self.backward(state)
        if EVENT_REDUCE_SPEED in actions:
            self.decelerate(state)
        if EVENT_LEFT in actions:
            self.rotate(state, -1)
        if EVENT_RIGHT in actions:
            self.rotate(state, 1)
        if EVENT_COLLISION in actions:
            self.bounce(state)
        if EVENT_QUIT in actions:
            self.quit(state)

    def forward(self, state):
        temp_player = state.players[state.player_id]
        audio.accelerateSound()
        temp_player.vel = min(temp_player.vel + temp_player.acceleration, temp_player.max_vel)
        self.move(state)

    def backward(self, state):
        temp_player = state.players[state.player_id]
        audio.accelerateSound()
        temp_player.vel = min(temp_player.vel - temp_player.acceleration, -temp_player.max_vel/2)
        self.move(state)

    def decelerate(self, state):
        temp_player = state.players[state.player_id]
        temp_player.vel = max(temp_player.vel - temp_player.acceleration / 2, 0)
        self.move(state)

    def rotate(self, state, direction):
        temp_player = state.players[state.player_id]
        temp_player.player_angle -= temp_player.angle_increment * direction
        state.players[0] = temp_player

    def move(self, state):
        temp_player = state.players[state.player_id]
        radians = math.radians(temp_player.player_angle)
        
        # Calculate the components based on player's velocity without the negative sign
        vertical = math.cos(radians) * temp_player.vel
        horizontal = math.sin(radians) * temp_player.vel

        # Update player's position
        temp_player.player_x += horizontal
        temp_player.player_y += vertical

        state.players[state.player_id] = temp_player
    
    def bounce(self, state):
        state.players[state.player_id].vel = -state.players[state.player_id].vel
        
    def quit(self, state):
        state.cycle = "quit"

    def addPlayer(self, state, ID, player):
        state.players[ID] = player
    
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
    # Initialize networking variables
    def __init__(self, type, ip, port):
        try:
            self.type = type
            self.host = ip
            self.port = port
            self.sock = None
            self.connected = []
            self.status = None
            self.receiveSize = 4096
        except:
            print("Initilization of networking Failed.")

    # Start the networking socket
    def start(self):
        if self.type == "server":
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock = s
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.host, self.port))
            s.listen()
            self.connected.append(s)
        else: 
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock = s
            s.connect((self.host, self.port))
        self.status = "active"

    # Receive data from the connected peers
    def receive(self):
        if self.status == "active":
            if self.type == "server":
                read_sockets, _, exception_sockets = select.select(self.connected, [], self.connected, 0)
                for notified_socket in read_sockets:
                    # New connection
                    if notified_socket == self.sock:
                        client_socket, client_address = self.sock.accept()
                        try:
                            message = client_socket.recv(self.receiveSize).decode()
                        except:
                            print("A client disconnected")
                            return None
                        
                        if message is False:
                            print("A client disconnected")
                            return None

                        self.connected.append(client_socket)
                        return message

                    # Existing client is sending a message
                    else:
                        try:
                            message = notified_socket.recv(self.receiveSize).decode()
                        except:
                            self.connected.remove(notified_socket)
                            print("A client disconnected")
                            return None

                        if message is False:
                            self.connected.remove(notified_socket)
                            print("A client disconnected")

                        for notified_socket in exception_sockets:
                            self.connected.remove(notified_socket)
                            print("A client disconnected")

                        return message
            else: 
                try:
                    message = self.sock.recv(self.receiveSize).decode()
                except:
                    print("The server disconnected")
                    self.status = "inactive"
                    return None
                
                if not message:
                    print("The server disconnected")
                    self.status = "inactive"
                    return None
                else:
                    return message

    # Send data to the connected peers
    def send(self, data):
        if self.status == "active":
            if self.type == "server":
                currentSock = None
                try:
                    if len(self.connected) > 1:
                        for client in range(1, len(self.connected)):
                            currentSock = self.connected[client]
                            self.connected[client].sendall(data.encode())
                except:
                    self.connected.remove(currentSock)
                    print("A client disconnected")
            else: 
                try:
                    self.sock.sendall(data.encode())
                except:
                    print("The server disconnected")
                    self.status = "inactive"
    
    # End the network socket connection
    def end(self):
        self.sock.close()

class audio(GameEngine):
    def startMusic():
        pass
    def accelerateSound():
        pygame.mixer.Sound.play(accel_sound)

class physics(GameEngine):
    pass
