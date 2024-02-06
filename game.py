# Tiny Turismo game and 2D top-down racing engine
# Made for Drexel CS 438
# Jack Pinkstone - jsp334@drexel.edu
# Noah Robinson - nkr38@drexel.edu
# Casssius Garcia - cag383@drexel.edu

from game_state import *
from game_engine import *

state = GameState()
engine = GameEngine(state)
isServer = True
serverIp = "127.0.0.1"

if isServer:
    Net = engine.networking("server", "127.0.0.1", 60217)
else:
    Net = engine.networking("client", serverIp, 60217)

def updateHUD():
    pass

# # uses the remainder of the frame time, returns the change in time
# def fpsControl(fps, startTime):
#     frameTime = 1/fps
#     dt = time.localtime() - startTime
#     while(dt < frameTime):
#         dt = time.localtime() - startTime
#     return dt

def mainLoop(send, receive):
    
    #------------------Main Game Loop------------------#
    while (state.status != "stopped"):
        startTime = time.localtime()

        # Get user input and update game state
        userInput = engine.input.getInput()
        GameActions(userInput)

        # Get other networking player states and update game state
        networkData = receive()
        if networkData != "None":
            state.unpack(networkData)

        # Send current game state to other networking players
        send(state.pack())

        # Update the HUD from the game state
        updateHUD()

        # Render the frame and do collisions and physics
        engine.render()

        # Try to keep the game running at a constant FPS
        # dt = fpsControl(30, startTime)
        engine.clock.tick(30)
    #--------------------------------------------------#
    pygame.quit()

if __name__ == '__main__':
    Net.start(mainLoop)
