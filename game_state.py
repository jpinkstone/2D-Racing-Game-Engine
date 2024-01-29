class GameState:
    # Initialize the total amount of players in the form of a list
    def __init__(self,players):
        try:
            self.players = []
            self.players = players
            self.total_players = len(self.players)
            self.delimiter = "|"
        except:
            print("Initilization of Game State Failed.")

    def UpdateGameState(UserInput):
        pass
        
    # Add a new player using PlayerGameState
    def add_players(self,player):
        self.players.append(player)
        print("New Player Added")

    def get_player_state(self, index):
        try:
            return self.players[index]
        except:
            print("ERROR: Developer trying to access a nonexistent player.")

    def get_total_players(self):
        self.total_players = len(self.players)
        return self.total_players
    
    def pack(self):
        encoded_data = ""
        
        for i in range(self.get_total_players()):
            player = self.players[i]
            player_data = vars(player)
            for j in player_data:
                encoded_data += str(player_data[j]) + self.delimiter

        return encoded_data

    def unpack(self,encoded_data):
        decoded_data = encoded_data.split(self.delimiter)
        j = 0
        for i in range(self.get_total_players()):
            player = self.players[i]
            player_data = vars(player)
            #print(player_data)
            for key in player_data:
                exec(f'self.players[{i}].{key}={decoded_data[j]}')
                j+=1

class PlayerGameState:
    def __init__(self,size, width,height):
        # Player car info
        self.player_size = size
        self.player_x = width
        self.player_y = height
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
    
    def get_loc(self):
        return self.player_x, self.player_y
    
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
    

# if __name__ == "__main__":
#     # Example:
#     #    Create four players, add another player, test the encoding and decoding for the 
#     WIDTH, HEIGHT = 800, 600
#     player_size = 50
#     total_players = 3
#     players = []

#     for i in range(total_players):      
#         players.append(PlayerGameState(player_size,WIDTH // 2 - player_size // 2,HEIGHT//2))
        
#     game_state = FullGameState(players)
#     total_size_bytes = 0
#     game_state.add_players(PlayerGameState(player_size,WIDTH // 2 - player_size // 2,HEIGHT//2))

#     print("Total Players: " + str(game_state.get_total_players()))
    
#     for i in range(game_state.get_total_players()):
#         player_state = game_state.get_player_state(i)
#         print("Game State of Player " + str(i) + ": " + str(player_state))

#     if(test_encoding_decoding(game_state)): print("Encoding and Decoding worked properly!")
