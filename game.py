# Main game loop file that calls the game engine
from game_state import *
from game_engine import *

State = GameState()
Engine = GameEngine()

while (!quit):
    startTime = time()
    # Get user input and update game state
    UserInput = getKeyboard()
    State.UpdateGameState(UserInput)

    # Get other networking player states and update game state
    NetworkInput = State.unpack(Engine.Networking.getData())
    State.UpdateGameState(NetworkInput)

    # Send current game state to other networking players
    Engine.Networking.sendData(State.pack())

    # Update the HUD from the game state
    updateHUD()

    # Render the frame and do collisions and physics
    Engine.Render()

    # Try to keep the game running at a constant FPS
    FPScontrol(30, startTime)

def getKeyboard():
    pass

def updateHUD():
    pass

def FPSControl(fps, startTime):
    pass
