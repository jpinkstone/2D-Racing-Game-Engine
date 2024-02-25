# Tiny Turismo game and 2D top-down racing engine
# Made for Drexel CS 438
# Jack Pinkstone - jsp334@drexel.edu
# Noah Robinson - nkr38@drexel.edu
# Casssius Garcia - cag383@drexel.edu

from game_state import *
from game_engine import *
from game_support import *

sprite = SPRITE_GREEN
isServer = True
serverIp = "127.0.0.1"
port = 60217

if isServer:
    net = networking("server", serverIp, port)
else:
    net = networking("client", serverIp, port)

pygame.init()
net.start()
state = GameState(isServer, sprite)
engine = GameEngine(state)

#------------------Main Game Loop------------------#
while (state.status != "stopped"):
    userData = getInput()             # Get user input

    net.send(state.pack())            # Send player and game data to connected players

    networkData = net.receive()       # Receive connected player data and update game
    if networkData != None:
        state.unpack(networkData)

    cycle(engine, state, userData)    # Update the game cycle

    engine.render()                   # Render the frame and do collisions and physics

    engine.clock.tick(30)             # Try to keep the game running at a constant FPS
#--------------------------------------------------#
    
pygame.quit()
net.end()
