# Main game loop file that calls the game engine
from game_state import *
from game_engine import *

State = GameState()
Engine = GameEngine()
isServer = True

while (!quit):
    startTime = time()
    # Get user input and update game state
    UserInput = getKeyboard()
    State.UpdateGameState(UserInput)

    # Get other networking player states and update game state
    if isServer:
        NetworkInput = State.unpack(Engine.NetworkingServer.getData())
    else:
        NetworkInput = State.unpack(Engine.NetworkingClient.getData())
    State.UpdateGameState(NetworkInput)

    # Send current game state to other networking players
    if isServer:
        Engine.NetworkingServer.sendData(State.pack())
    else:
        Engine.NetworkingClient.sendData(State.pack())

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
