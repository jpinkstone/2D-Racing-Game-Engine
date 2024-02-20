import uuid

ACCELERATION_FACTOR = 0.1
ROTATION_INCREMENT = 5
MAX_VELOCITY = 5

class GameState:
    # Initialize the total amount of players in the form of a list
    def __init__(self, isServer):
        try:
            self.title = "Tiny Turismo"
            self.players = []
            self.delimiter = "|"
            self.status = "running"
            self.cycle = "menu"
            self.isServer = isServer
            self.player_id = uuid.UUID(int=uuid.getnode()) # Why UUID? TypeError: list indices must be integers or slices, not UUID
            self.map = "track.png"
            self.mapMask = "track_mask.png"
            self.playerSprites = ["race_car0.png", "race_car1.png", "race_car2.png", "race_car3.png"]
            self.dimensions = (1920*0.75, 1080*0.75)
            self.gameTime = None
            self.lastTime = None
            self.firstPlace = None
        except:
            print("Initilization of Game State Failed.")
    
    def pack(self):
        encoded_data = ""

        game_state_vars = vars(self)

        for key in game_state_vars.keys():
            if key != 'status': continue
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

class PlayerGameState:
    def __init__(self, id, width, height):
        # Player car info
        self.dimensions = (width, height)
        self.player_id = id
        self.player_x = 600
        self.player_y = 650
        self.score = 0
        self.sprite_id = 0
        # Movement
        self.vel = 0
        self.player_angle = 90
        self.max_vel = MAX_VELOCITY
        self.acceleration = ACCELERATION_FACTOR
        self.angle_increment = ROTATION_INCREMENT