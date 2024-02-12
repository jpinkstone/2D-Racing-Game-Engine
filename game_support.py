from game_engine import *

def getInput():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return "quit"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                return "accelF"
            if event.key == pygame.K_s:
                return "accelB"
            if event.key == pygame.K_a:
                return "left"
            if event.key == pygame.K_d:
                return "right"
            if event.key == pygame.K_r:
                return "restart"
            if event.key == pygame.K_RETURN:
                return "enter"
            if event.key == pygame.K_q:
                return "quit"
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                return "decelF"
            if event.key == pygame.K_s:
                return "decelB"
            
def cycle(engine, state, userData):
    if state.cycle == "menu": menu_state(engine, state, userData)
    elif state.cycle == "startup": startup_state(engine, state, userData)
    elif state.cycle == "game": game_state(engine, state, userData)
    elif state.cycle == "done": done_state(engine, state, userData)
    elif state.cycle == "quit": quit_state(engine, state, userData)

def menu_state(engine, state, userData):
    # Update game state
    # Do stuff
    # Add stuff to screen (Don't render. Happens in main loop)
    fill(engine, (200, 200, 200))
    addText(engine, state.dimensions[0]/2, state.dimensions[1]/3, 'freesansbold.ttf', 32, state.title)
    addText(engine, state.dimensions[0]/2, state.dimensions[1]/2, 'freesansbold.ttf', 32, "Press 'Enter' to begin game")
    addText(engine, state.dimensions[0]/2, state.dimensions[1]/4, 'freesansbold.ttf', 32, "Currently connected peer players: " + str(len(state.players)))
    if userData == "enter":
        state.cycle = "startup"
    elif userData == "quit":
        state.status = "stopped"

def startup_state(engine, state, userData):
    # Update game state
    # Do stuff
    # Add stuff to screen (Don't render. Happens in main loop)
    clear(engine)
    player = PlayerGameState(state.playerId+1,500,500)
    EngineActions.addPlayer(state, player)
    audio.startMusic()
    EngineActions.setGameTime(state, 180)
    EngineActions.setLastTime(state, int(datetime.datetime.today().timestamp()))
    state.cycle = "game"

def game_state(engine, state, userData):
    # Update game state
    # Do stuff
    # Add stuff to screen (Don't render. Happens in main loop)
    clear(engine)
    addMap(engine, "/assets/track.png", state.dimensions)
    GameActions(state, userData)
    addText(engine, state.dimensions[0]-125, 25, 'freesansbold.ttf', 32, "Time left: " + str(state.gameTime))
    if int(datetime.datetime.today().timestamp()) > state.lastTime:
        EngineActions.setLastTime(state, int(datetime.datetime.today().timestamp()))
        EngineActions.decreaseGameTime(state, 1)
    if state.gameTime <= 0:
        state.cycle = "done"
    if userData == "quit":
        state.status = "stopped"

def done_state(engine, state, userData):
    # Update game state
    # Do stuff
    # Add stuff to screen (Don't render. Happens in main loop)
    clear()
    fill((200, 200, 200))
    addText(engine, state.dimensions[0]/2, state.dimensions[1]/2, 'freesansbold.ttf', 32, "Player " + state.firstPlace + " wins!")
    addText(engine, state.dimensions[0]/2, state.dimensions[1]/3, 'freesansbold.ttf', 32, "Press 'q' to exit game")
    addText(engine, state.dimensions[0]/2, state.dimensions[1]/3, 'freesansbold.ttf', 32, "Press 'r' to restart game")
    if userData == "quit":
        state.status = "stopped"
    elif userData == "r":
        state.cycle = "startup"

def quit_state(engine, state, userData):
    # Update game state
    # Do stuff
    # Add stuff to screen (Don't render. Happens in main loop)
    clear()
    fill((200, 200, 200))
    addText(engine, state.dimensions[0]/2, state.dimensions[1]/3, 'freesansbold.ttf', 32, "Press 'q' to exit game")
    if userData == "quit":
        state.status = "stopped"
