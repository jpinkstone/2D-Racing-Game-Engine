# Tiny Turismo game and 2D top-down racing engine
# Made for Drexel CS 438
# Jack Pinkstone - jsp334@drexel.edu
# Noah Robinson - nkr38@drexel.edu
# Casssius Garcia - cag383@drexel.edu

from game_state import *
from game_engine import *
from game_support import *

state = GameState()
engine = GameEngine(state)
isServer = True
serverIp = "127.0.0.1"

if isServer:
    Net = engine.networking("server", "127.0.0.1", 60217)
else:
    Net = engine.networking("client", serverIp, 60217)

def mainLoop(send, receive):
    
    #------------------Main Game Loop------------------#
    while (state.status != "stopped"):
        # Get user input
        userData = getInput()

        # Get other networking player states and update game state
        networkData = receive()
        if networkData != "None":
            state.unpack(networkData)

        # Send current game state to other networking players
        send(state.pack())

        # Update the game cycle
        cycle(engine, state, userData)

        # Render the frame and do collisions and physics
        engine.render()

        # Try to keep the game running at a constant FPS
        engine.clock.tick(30)
    #--------------------------------------------------#
    pygame.quit()

if __name__ == '__main__':
    Net.start(mainLoop)
