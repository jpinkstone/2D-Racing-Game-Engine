import socket
import select
import math
import sys
import datetime
import random
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from pygame import mixer
from game_state import *

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
        if player.sprite_id != None: 
            img_rect = self.assets[player.sprite_id].get_rect()
            rotated = pygame.transform.rotate(self.assets[player.sprite_id], player.player_angle)
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

    def updateCarPositions(self, state, Path):
        distances = []

        for id in state.players.keys():
            closest_waypoint_index = min(range(len(Path)), key=lambda i: math.sqrt((Path[i][0] - state.players[id].player_x)**2 + (Path[i][1] - state.players[id].player_y)**2))
            distances.append((id, closest_waypoint_index))

        for ai_player in state.playersAI:
            closest_waypoint_index = min(range(len(Path)), key=lambda i: math.sqrt((Path[i][0] - ai_player.player_x)**2 + (Path[i][1] - ai_player.player_y)**2))
            distances.append((ai_player.id, closest_waypoint_index))
            
        sorted_cars = sorted(distances, key=lambda x: x[1], reverse=True)
        state.car_order = [state.player_names.get(int(car[0]), None) for car in sorted_cars]
        state.car_order = [car for car in state.car_order if car is not None]
        print(state.car_order)

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
        audio.accelerateSound("accelerate.wav", 0.2)
        temp_player.vel = min(temp_player.vel + temp_player.acceleration, temp_player.max_vel)
        self.move(state)

    def backward(self, state):
        temp_player = state.players[state.player_id]
        audio.accelerateSound("accelerate.wav", 0.2)
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
        
        vertical = math.cos(radians) * temp_player.vel
        horizontal = math.sin(radians) * temp_player.vel

        temp_player.player_x += horizontal
        temp_player.player_y += vertical

        state.players[state.player_id] = temp_player
    
    def bounce(self, state):
        state.players[state.player_id].vel = -state.players[state.player_id].vel
        
    def quit(self, state):
        state.cycle = "quit"

    def addPlayer(self, state, ID, player):
        state.players[ID] = player
        state.player_names[ID] = f"Player {len(state.player_names) + 1}"

    def addPlayerAI(self, state, player):
        ai_player_id = len(state.playersAI) + 1
        state.playersAI.append(player)
        state.player_names[ai_player_id] = f"AI {len(state.playersAI)}"
    
    def setGameTime(self, state, seconds):
        state.gameTime = seconds

    def setLastTime(self, state, time):
        state.lastTime = time
    
    def decreaseGameTime(self, state, num):
        state.gameTime -= num
    
class PlayerAI(PlayerGameState):
    def __init__(self, path, velocity, max_velocity):
        super().__init__()
        self.path = path
        self.id = None
        self.current_waypoint = None
        self.vel = velocity
        self.max_vel = max_velocity
        self.player_angle = 90
        self.angle_increment = 10

    def follow_waypoints(self):
        if not self.current_waypoint:
            self.current_waypoint = self.path[0]

        if self.distance_to_waypoint() < 5:
            self.current_waypoint = self.path[(self.path.index(self.current_waypoint) + 1) % len(self.path)]
            # print("cur waypoint " + str(self.current_waypoint[0]) +  " "  + str(self.current_waypoint[1]))
        self.move_towards(self.current_waypoint)

    def distance_to_waypoint(self):
        if self.current_waypoint:
            # dist = math.sqrt((self.current_waypoint[0] - self.player_x)**2 + (self.current_waypoint[1] - self.player_y)**2)
            # print(dist)
            return math.sqrt((self.current_waypoint[0] - self.player_x)**2 + (self.current_waypoint[1] - self.player_y)**2)
        return float('inf')

    def move_towards(self, waypoint):
        angle_to_target = math.atan2(waypoint[0] - self.player_x, waypoint[1] - self.player_y)
        angle_difference = math.degrees(angle_to_target) - self.player_angle

        if angle_difference > 180:
            angle_difference -= 360
        elif angle_difference < -180:
            angle_difference += 360

        rotation_direction = 1 if angle_difference > 0 else -1
        rotation_amount = min(abs(angle_difference), self.angle_increment)

        self.rotate(rotation_direction * rotation_amount)
        self.forward()

    def forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def rotate(self, angle_difference):
        self.player_angle += angle_difference

    def move(self):
        radians = math.radians(self.player_angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.player_x += horizontal
        self.player_y += vertical

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
            self.receiveSize = 2048
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
    def init():
        mixer.init()

    def startMusic():
        pass

    def accelerateSound(file, volume):
        accel_sound = pygame.mixer.Sound(os.path.join("assets", file))
        accel_sound.set_volume(volume)
        pygame.mixer.Sound.play(accel_sound)

class physics(GameEngine):
    pass