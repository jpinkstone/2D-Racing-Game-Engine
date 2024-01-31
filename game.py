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
    while running:
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
        if keys[pygame.K_RIGHT]:
            # player_angle -= 5  # Rotate right

def updateHUD():
    pass

def FPSControl(fps, startTime):
    pass
