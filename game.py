# Tiny Turismo game and 2D top-down racing engine
# Made for Drexel CS 438
# Jack Pinkstone - jsp334@drexel.edu
# Noah Robinson - nkr38@drexel.edu
# Casssius Garcia - cag383@drexel.edu

from game_state import *
from game_engine import *
from game_support import *

isServer = True
serverIp = "127.0.0.1"
port = 60217

if isServer:
    net = networking("server", "127.0.0.1", port)
else:
    net = networking("client", serverIp, port)

pygame.init()
net.start()
state = GameState(isServer)
engine = GameEngine(state)

#------------------Main Game Loop------------------#
while (state.status != "stopped"):
    userData = getInput()             # Get user input

    stateData = state.pack()
    print(stateData)

    net.send(stateData)

    networkData = net.receive()       # Get other networking player states and update game state
    if networkData != None:
        state.unpack(networkData)

    cycle(engine, state, userData)    # Update the game cycle

    engine.render()                   # Render the frame and do collisions and physics

    engine.clock.tick(30)             # Try to keep the game running at a constant FPS
#--------------------------------------------------#
    
pygame.quit()
net.end()
