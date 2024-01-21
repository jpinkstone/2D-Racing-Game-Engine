# import sys

class FullGameState:
    # Initialize the total amount of players in the form of a list
    def __init__(self,players):
        try:
            self.players = []
            self.players = players
            self.total_players = len(self.players)
        except:
            print("Initilization of Game State Failed.")

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
    
    def get_loc(self):
        return self.player_x, self.player_y
    


if __name__ == "__main__":
    # Example: create four players, add another player, get the total size in bytes
    WIDTH, HEIGHT = 800, 600
    player_size = 50
    total_players = 4
    players = []

    for i in range(total_players):      
        players.append(PlayerGameState(player_size,WIDTH // 2 - player_size // 2,HEIGHT//2))
        
    game_state = FullGameState(players)
    total_size_bytes = 0
    game_state.add_players(PlayerGameState(player_size,WIDTH // 2 - player_size // 2,HEIGHT//2))
    
    for i in range(game_state.get_total_players()):
        player_state = game_state.get_player_state(i)
        # state_size = sys.getsizeof(player_state)
        print("Game State of Player " + str(i) + ": " + str(player_state))
        # print("Size of Player " + str(i) + " State in bytes: " + str(sys.getsizeof(player_state)))

    print("Total Players: " + str(game_state.get_total_players()))
    # print("Total Size (bytes): " + str(sys.getsizeof(game_state)))