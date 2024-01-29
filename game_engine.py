import pygame
import sys
from game_state import *
import keyboard

class GameEngine():
    def __init__(self):
        try:
            self.game_state = FullGameState()
        except:
            print("Initilization of Game Engine Failed.")

    def add_player(self):
        player = PlayerGameState()
        self.game_state.add_player(player)

    def get_game_state(self):
        return self.game_state
    
    def update_game_state(self, game_state):
        self.game_state = game_state

    def receive_game_state(self):
        # function of whatever networking class
        pass

    def send_game_state(self):
        # function of whatever networking class
        pass

    def get_keyboard_input(self):
        pass
        
    class Multiplayer():
        pass
    class Render():
        pass
    class GameAI():
        pass
    class Physics():
        pass
