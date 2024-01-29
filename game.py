# Main game loop file that calls the game engine

from game_state import *
from game_engine import *
from keyboard import *

State = FullGameState()
Engine = GameEngine()

while (!quit):
    NewInput = keyboard()
    State.UpdateGameState(NewInput)
    Engine.Render()
    FPScontrol()