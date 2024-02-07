class GameState:
    # Initialize the total amount of players in the form of a list
    def __init__(self,players = []):
        try:
            self.title = "Tiny Turismo"
            self.players = players
            self.delimiter = "|"
            self.status = "running"
            self.cycle = "menu"
            self.playerId = len(self.players) + 1
            self.map = "assets/track.png"
            self.mapMask = "assets/track_mask.png"
            self.playerSprites = ["race_car_blue.png", "race_car_green.png", "race_car_pink.png", "race_car_red.png"]
            self.dimensions = (1000, 800)
            print(vars(self))
        except:
            print("Initilization of Game State Failed.")
    
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
