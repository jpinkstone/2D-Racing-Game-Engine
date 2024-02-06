import pygame
import math

class GameState:
    # Initialize the total amount of players in the form of a list
    def __init__(self,players = []):
        try:
            self.title = "Tiny Turismo"
            self.players = players
            self.delimiter = "|"
            self.status = 1
            self.playerId = len(self.players) + 1
            self.map = "assets/track.png"
            self.mapMask = "assets/track_mask.png"
            self.playerSprites = ["race_car_blue.png", "race_car_green.png", "race_car_pink.png", "race_car_red.png"]
            self.screen = (1000, 800)
            print(vars(self))
        except:
            print("Initilization of Game State Failed.")

    def addPlayer(self,player):
        self.players.append(player)
    
    def pack(self):
        encoded_data = ""

        game_state_vars = vars(self)

        for key in game_state_vars.keys():
            if key == 'players' or key == 'delimiter': continue
            encoded_data += str(game_state_vars[key]) + self.delimiter
        
        for i in range(len(self.players)):
            player = self.players[i]
            player_data = vars(player)
            for j in player_data:
                encoded_data += str(player_data[j]) + self.delimiter

        return encoded_data

    def unpack(self,encoded_data):
        decoded_data = encoded_data.split(self.delimiter)
        game_state_vars = vars(self)
        print(game_state_vars)
        j = 0
        for key in game_state_vars.keys():
            if key == 'players' or key == 'delimiter': continue
            exec(f'self.{key}={decoded_data[j]}')
            j = j + 1
        
        for i in range(len(self.players)):
            player = self.players[i]
            player_data = vars(player)
            #print(player_data)
            for key in player_data:
                exec(f'self.players[{i}].{key}={decoded_data[j]}')
                j+=1
    
    # FIXME: Function meant to sync data of different player states
    # for example: changing player id's within the game state
    def sync(self):
        pass

class PlayerGameState:
    def __init__(self, id, width, height):
        # Player car info
        self.width = width
        self.height = height
        self.playerId = id
        self.player_x = 50
        self.player_y = 50
        self.player_speed = 1
        self.player_max_speed = 5  # Increased max speed
        self.acceleration = 1.0  # Increased acceleration
        self.deceleration_factor = 0.2
        self.player_velocity = [0, 0]
        self.player_angle = 0  # Initial angle in degrees
        self.accelerating = False  # Flag to track if accelerating
        self.decelerating = False  # Flag to track if decelerating
        self.player_velocity[0] = 0
        self.player_velocity[1] = 0
        self.score = 0

class CarAI(playerGameState):
    def __init__(self, max_vel, rotation_vel, path=[]):
        super().__init__(max_vel, rotation_vel)
        self.path = path
        self.current_point = 0
        self.vel = max_vel

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

class GameActions():
    def __init__(self, action): 
        if action == "accelF": self.accelF()
        elif action == "accelB": self.accelB()
        elif action == "decelF": self.decelF()
        elif action == "decelB" : self.decelB()
        elif action == "left": self.left()
        elif action == "right": self.right()
        elif action == "quit": self.quit()

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
        pass
    
# def test_encoding_decoding(game_state):
#     before_encoding = []
#     after_encoding = []
#     for i in range(game_state.get_total_players()):
#         before_encoding.append(vars(game_state.get_player_state(i)))

#     encoded_data = game_state.encode_data()
#     game_state.decode_data(encoded_data)

#     for i in range(game_state.get_total_players()):
#         after_encoding.append(vars(game_state.get_player_state(i)))

#     # Compare the dictionaries of the variables and see if they work
#     def dict_compare(d1, d2):
#         d1_keys = set(d1.keys())
#         d2_keys = set(d2.keys())
#         shared_keys = d1_keys.intersection(d2_keys)
#         added = d1_keys - d2_keys
#         removed = d2_keys - d1_keys
#         modified = {o : (d1[o], d2[o]) for o in shared_keys if d1[o] != d2[o]}
#         same = set(o for o in shared_keys if d1[o] == d2[o])
#         return added, removed, modified, same
    
#     for i in range(len(after_encoding)):
#         added, removed, modified, same = dict_compare(before_encoding[i], after_encoding[i])
#         if (len(added)+len(removed)+len(modified)!=0): return False
    
#     return True
    

if __name__ == "__main__":
    # Example:
    #    Create four players, add another player, test the encoding and decoding for the 
    WIDTH, HEIGHT = 800, 600
    player_size = 50
      
    game_state = GameState()
    total_size_bytes = 0
    game_state.addPlayer(PlayerGameState(1,WIDTH // 2 - player_size // 2,HEIGHT//2))

    packed = game_state.pack()
    game_state.unpack(packed)
    print(vars(game_state.players[0]))
    #print(vars(game_state))
    
    #if(test_encoding_decoding(game_state)): print("Encoding and Decoding worked properly!")
