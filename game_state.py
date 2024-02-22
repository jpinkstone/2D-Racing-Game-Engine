import uuid
import re

ACCELERATION_FACTOR = 0.1
ROTATION_INCREMENT = 5
MAX_VELOCITY = 5

class GameState:
    # Initialize the total amount of players in the form of a list
    def __init__(self, isServer):
        try:
            self.title = "Tiny Turismo"
            self.players = {}
            self.delimiter = "|"
            self.status = "running"
            self.cycle = "menu"
            self.isServer = isServer
            self.player_id = uuid.UUID(int=uuid.getnode()).int
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

        # Pack the game state variables
        encoded_data += self.pack_game_state()
        
        # Pack variables for every player
        for id, player in self.players.items():
            encoded_data += self.pack_player_state(id,player)

        return encoded_data
    
    def pack_game_state(self):
        encoded_data = ""
        game_state_vars = vars(self)
        # Pack the game state variables
        for key in game_state_vars.keys():
            if key != 'status': continue
            encoded_data += str(game_state_vars[key]) + self.delimiter
        return encoded_data

    def pack_player_state(self,id,player):
        encoded_data = "{" + str(id) + "|"
        player_data = vars(player)
        
        for var in player_data:
            encoded_data += str(player_data[var]) + self.delimiter
        encoded_data += "}"
        return encoded_data

    def unpack(self,encoded_data):
        player_states, encoded_data = self.extract_player_states(encoded_data)
        decoded_data = encoded_data.split(self.delimiter)
        # Unpack the game state variables
        self.unpack_game_state(decoded_data)
        
        # Unpack variables for every player
        for player_data in player_states:
            if self.is_new_player(player_states):
                self.unpack_new_player_state(player_data)
            else:
                self.unpack_player_state(player_data)

    # Returns a list of undelimited player data for all players
    def extract_player_states(self,encoded_data):
        pattern = r'\{([^}]*)\}'  # Regular expression to match content within curly braces
        matches = re.findall(pattern, encoded_data)
        result_string = re.sub(pattern, '', encoded_data)
        return matches, result_string

    def unpack_game_state(self,decoded_data):
        game_state_vars = vars(self)
        for key in game_state_vars.keys():
            if key == 'status':
                setattr(self,key,decoded_data[0])

    def is_new_player(self,player_data):
        player_var_values = player_data.split(self.delimiter)
        id = uuid.UUID(player_var_values[0].strip()).int
        if id in self.players:
            return 0
        return 1
    
    def unpack_new_player_state(self,new_player_data):
        new_player_var_values = new_player_data.split(self.delimiter)
        id = uuid.UUID(new_player_var_values[0].strip()).int
        del new_player_var_values[0]
        try:    
            new_player = PlayerGameState(60, 60)
            new_player_var_names = vars(new_player)
            for name, value in zip(new_player_var_names, new_player_var_values):
                exec(f'new_player.{name} = {value}')
            self.players[id] = new_player
        except KeyError:
            print("Player not found")
        except Exception as e:
            print(f"Error unpacking player: {e}")

    def unpack_player_state(self,player_data):
        player_var_values = player_data.split(self.delimiter)
        id = uuid.UUID(player_var_values[0].strip()).int
        del player_var_values[0]
        try:    
            player = self.players[id]
            player_var_names = vars(player)
            for name, value in zip(player_var_names, player_var_values):
                exec(f'player.{name} = {value}')
            self.players[id] = player
        except KeyError:
            print("Player not found")
        except Exception as e:
            print(f"Error unpacking player: {e}")


class PlayerGameState:
    def __init__(self, width, height):
        # Player car info
        self.dimensions = (width, height)
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