# Main game loop file
from game_state import *
from game_engine import *

State = GameState()
Engine = GameEngine()
isServer = True
serverIp = "127.0.0.1"

if isServer:
    Net = Engine.networkingClass("server", "127.0.0.1", 60217)
else:
    Net = Engine.networkingClass("client", serverIp, 60217)

def getKeyboard():
    while running:
        pass
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                accelerating = True
            elif event.key == pygame.K_DOWN:
                decelerating = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                accelerating = False
            elif event.key == pygame.K_DOWN:
                decelerating = False
        if keys[pygame.K_LEFT]:
            # player_angle += 5  # Rotate left
            pass
        if keys[pygame.K_RIGHT]:
            # player_angle -= 5  # Rotate right
            pass

def updateHUD():
    pass

def FPSControl(fps, startTime):
    pass

def mainLoop(send, receive):
    while (not quit):
        startTime = time()
        # Get user input and update game state
        UserInput = getKeyboard()
        State.UpdateGameState(UserInput)

        # Get other networking player states and update game state
        NetworkInput = State.unpack(receive())
        State.UpdateGameState(NetworkInput)

        # Send current game state to other networking players
        send(State.pack())

        # Update the HUD from the game state
        updateHUD()

        # Render the frame and do collisions and physics
        Engine.Render()

        # Try to keep the game running at a constant FPS
        FPSControl(30, startTime)

if __name__ == '__main__':
    Net.start(mainLoop)
