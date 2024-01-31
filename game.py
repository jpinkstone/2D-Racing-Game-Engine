# Tiny Turismo game and 2D top-down racing engine
# Made for Drexel CS 438
# Jack Pinkstone - jsp334@drexel.edu
# Noah Robinson - nkr38@drexel.edu
# Casssius Garcia - cag383@drexel.edu

from game_state import *
from game_engine import *

state = GameState()
engine = GameEngine()
isServer = True
serverIp = "127.0.0.1"

if isServer:
    Net = engine.networking("server", "127.0.0.1", 60217)
else:
    Net = engine.networking("client", serverIp, 60217)

def getInput():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return "stopped"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                return "acceleratingF"
            if event.key == pygame.K_s:
                return "acceleratingB"
            if event.key == pygame.K_a:
                return "left"
            if event.key == pygame.K_d:
                return "right"
            if event.key == pygame.K_q:
                return "stopped"
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                return "deceleratingF"
            if event.key == pygame.K_s:
                return "deceleratingB"

def updateHUD():
    pass

def fpsControl(fps, startTime):
    pass

def mainLoop(send, receive):
    
    #------------------Main Game Loop------------------#
    while (state.status != "stopped"):
        startTime = time.localtime()
        # Get user input and update game state
        userInput = getInput()
        state.UpdateGameState("keyboard", userInput)

        # Get other networking player states and update game state
        networkData = receive()
        if networkData != "None":
            state.UpdateGameState("network", networkData)

        # Send current game state to other networking players
        send(state.pack())

        # Update the HUD from the game state
        updateHUD()

        # Render the frame and do collisions and physics
        engine.render()

        # Try to keep the game running at a constant FPS
        fpsControl(30, startTime)
    #--------------------------------------------------#

if __name__ == '__main__':
    Net.start(mainLoop)
