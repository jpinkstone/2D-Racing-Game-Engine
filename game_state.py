import uuid
import re

ACCELERATION_FACTOR = 0.1
ROTATION_INCREMENT = 5
MAX_VELOCITY = 5

class GameState:
    # Initialize the total amount of players in the form of a list
    def __init__(self, isServer, sprite_id):
        try:
            self.title = "Tiny Turismo"
            self.players = {}
            self.playersAI = []
            self.car_order = []
            self.player_names = {}
            self.delimiter = "|"
            self.status = "running"
            self.cycle = "menu"
            self.startup = False
            self.isServer = isServer
            self.sprite_id = sprite_id
            self.player_id = uuid.uuid4().int
            self.map = "track.png"
            self.mapMask = "track_mask.png"
            self.playerSprites = ["race_car0.png", "race_car1.png", "race_car2.png", "race_car3.png"]
            self.dimensions = (1920*0.75, 1080*0.75)
            self.gameTime = 0
            self.lastTime = 0
            self.firstPlace = 0
            self.network_vars = ['status','car_order','lastTime','firstPlace','gameTime','cycle']
            self.time_vars = ['lastTime','firstPlace','gameTime']
        except:
            print("Initilization of Game State Failed.")
    
    def pack(self):
        encoded_data = ""

        # Pack the game state variables
        if self.isServer:
            encoded_data += self.pack_game_state()
            
        # Pack variables for local player
        if self.players:
            if self.player_id in self.players.keys():
                encoded_data += self.pack_player_state(self.player_id,self.players[self.player_id])
            else:
                encoded_data += "<" + str(self.player_id) + ">"  
        else:
            encoded_data += "<" + str(self.player_id) + ">"

        if self.isServer:
            for ai in self.playersAI:
                encoded_data += self.pack_ai(ai)

        return encoded_data
    
    # Pack the game state variables
    def pack_game_state(self):
        encoded_data = ""
        game_state_vars = vars(self)
        
        for key in game_state_vars.keys():
            if key in self.network_vars: 
                value = game_state_vars[key]
                if isinstance(value,str):
                    value = '"' + value + '"'
                if value == []: 
                    value = "[]"
                if value == {}: 
                    value = "{}"
                encoded_data += str(key) + "=" + str(value) + self.delimiter
        encoded_data = encoded_data[:-1]
        return encoded_data

    # Pack the player state variables
    def pack_player_state(self,id,player):
        encoded_data = "<" + str(id) + self.delimiter
        player_data = vars(player)
        
        for var in player_data:
            if var in player.network_vars:
                value = player_data[var]
                if isinstance(value,str): value = '"' + value + '"'
                encoded_data += str(var) + "=" + str(value) + self.delimiter
        encoded_data = encoded_data[:-1] + ">"
        return encoded_data
    
    # Pack the AI state variables
    def pack_ai(self,ai):
        encoded_data = "("
        ai_data = vars(ai)
        for var in ai_data:
            if var in ai.network_vars:
                value = ai_data[var]
                if isinstance(value,str): 
                    value = '"' + value + '"'
                encoded_data += str(var) + "=" + str(value) + self.delimiter
        
        encoded_data = encoded_data[:-1] + ")"
        return encoded_data

    def unpack(self,encoded_data):
        player_states, encoded_data = self.extract_player_states(encoded_data)
        ai_states, encoded_data = self.extract_ai_states(encoded_data)
        decoded_data = encoded_data.split(self.delimiter)

        # Unpack the game state variables
        if self.isServer == False:
            self.unpack_game_state(decoded_data)
            for i in range(len(ai_states)):
                if i > 3: break
                if i + 1 > len(self.playersAI):
                    self.unpack_new_ai(ai_states[i])
                else:
                    self.unpack_ai(ai_states[i], i)
        
        # Unpack variables for every player
        for player_data in player_states:
            if self.is_new_player(player_data):
                self.unpack_new_player_state(player_data)
            else:
                self.unpack_player_state(player_data)

    # Returns a list of undelimited player data for all players
    def extract_player_states(self, encoded_data):
        pattern = r'<([^>]*)>'  # Updated regular expression to match content within angle brackets
        matches = re.findall(pattern, encoded_data)
        result_string = re.sub(pattern, self.delimiter, encoded_data)
        return matches, result_string
    
    def extract_ai_states(self, encoded_data):
        pattern = r'\(([^)]*)\)'  # Updated regular expression to match content within parentheses
        matches = re.findall(pattern, encoded_data)
        result_string = re.sub(pattern, self.delimiter, encoded_data)
        return matches, result_string
    
    def unpack_new_ai(self,ai_data):
        ai_data = ai_data.split(self.delimiter)
        
        try:    
            new_ai = PlayerGameState(60,60)
            for expr in ai_data:
                exec(f'new_ai.{expr}')
            self.playersAI.append(new_ai)
        except KeyError:
            print("AI not found")
        except Exception as e:
            print(f"Error unpacking new AI: {e}")
        except:
            pass

    def unpack_ai(self,ai_data,index):
        ai_data = ai_data.split(self.delimiter)
        ai = self.playersAI[index]
        
        try:
            for expr in ai_data:
                exec(f'ai.{expr}')
            self.playersAI[index] = ai
        except KeyError:
            print("AI not found")
        except Exception as e:
            print(f"Error unpacking AI: {e}")
        except:
            pass

    def unpack_game_state(self,decoded_data):
        game_state_vars = vars(self)
        i = 0
        for expr in decoded_data:
            if not expr: continue
            try:
                exec(f'self.{expr}')
            except:
                pass
            
    def is_new_player(self,player_data):
        player_data = player_data.split(self.delimiter)
        id_string = player_data[0].strip()
        id = uuid.UUID(int=int(id_string)).int
        if id in self.players:
            return 0
        return 1
    
    def unpack_new_player_state(self,new_player_data):
        new_player_data = new_player_data.split(self.delimiter)
        id_string = new_player_data[0].strip()
        if id_string =='0':
            return
        id = uuid.UUID(int=int(id_string)).int
        del new_player_data[0]
        
        try:    
            new_player = PlayerGameState(60, 60)
            for expr in new_player_data:
                try:
                    exec(f'new_player.{expr}')
                except:
                    pass
            self.players[id] = new_player
        except KeyError:
            print("Player not found")
        except Exception as e:
            print(f"Error unpacking new player: {e}")
        except:
            pass

    def unpack_player_state(self,player_data):
        player_data = player_data.split(self.delimiter)
        id_string = player_data[0].strip()
        id = uuid.UUID(int=int(id_string)).int
        del player_data[0]
        try:    
            player = self.players[id]
            for expr in player_data:
                try:
                    exec(f'player.{expr}')
                except:
                    pass
            self.players[id] = player
        except KeyError:
            print("Player not found")
        except Exception as e:
            print(f"Error unpacking player: {e}")


class PlayerGameState:
    def __init__(self, width=60, height=60):
        # Player car info
        self.dimensions = (width, height)
        self.player_x = 600
        self.player_y = 650
        self.checkpoint_reached = False
        self.sprite_id = None
        # Movement
        self.vel = 0
        self.player_angle = 90
        self.max_vel = MAX_VELOCITY
        self.acceleration = ACCELERATION_FACTOR
        self.angle_increment = ROTATION_INCREMENT
        self.network_vars = ['player_x','player_y','score','sprite_id','player_angle']

    def player_set_network_vars(self,list_of_var_names):
        self.network_vars = list_of_var_names
