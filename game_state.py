class GameState:
    # Initialize the total amount of players in the form of a list
    def __init__(self,players = []):
        try:
            self.players = players
            self.delimiter = "|"
            self.status = 1
            self.playerId = len(self.players) + 1
            print(vars(self))
        except:
            print("Initilization of Game State Failed.")

    def addPlayer(self,player):
        self.players.append(player)

    def updateGameState(self, type, inputData):
        if type == "keyboard":
            if inputData == "stopped":
                self.status = "stopped"
            elif inputData == "acceleratingF":
                self.players[self.playerId].acceleration = self.players[self.playerId].acceleration + 1
            elif inputData == "deceleratingF":
                self.players[self.playerId].acceleration = self.players[self.playerId].acceleration - 1
            elif inputData == "acceleratingB":
                self.players[self.playerId].acceleration = self.players[self.playerId].acceleration - 1
            elif inputData == "deceleratingB":
                self.players[self.playerId].acceleration = self.players[self.playerId].acceleration + 1
            elif inputData == "left":
                self.players[self.playerId].angle = self.players[self.playerId].angle - 5
            elif inputData == "right":
                self.players[self.playerId].angle = self.players[self.playerId].angle + 5
        else:
            self.unpack(inputData)
    
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
