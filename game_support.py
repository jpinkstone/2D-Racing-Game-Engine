from game_engine import *

def getInput():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return EVENT_QUIT
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                return EVENT_ACCELF
            if event.key == pygame.K_s:
                return EVENT_ACCELB
            if event.key == pygame.K_a:
                return EVENT_LEFT
            if event.key == pygame.K_d:
                return EVENT_RIGHT
            if event.key == pygame.K_r:
                return EVENT_RESTART
            if event.key == pygame.K_RETURN:
                return EVENT_ENTER
            if event.key == pygame.K_q:
                return EVENT_QUIT
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                return EVENT_DECELF
            if event.key == pygame.K_s:
                return EVENT_DECELB
            
            
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
    addMap(engine, "/assets/track.png")
    player = PlayerGameState(state.playerId+1,500,500)
    EngineActions.addPlayer(EngineActions, state, player)
    # engine.audio.startMusic()
    # engine.EngineActions.startGame()
    # engine.cycle = "game"

def game_state(engine, state, userData):
    # Update game state
    # Do stuff
    # Add stuff to screen (Don't render. Happens in main loop)
    engine.GameActions(userData)
    engine.physics()
    if engine.timeLeft <= 0:
        engine.cycle = "done"

def done_state(engine, state, userData):
    # Update game state
    # Do stuff
    # Add stuff to screen (Don't render. Happens in main loop)
    engine.window.clear()
    engine.window.fill((200, 200, 200))
    engine.window.addText(engine.dimensions[0]/2, engine.dimensions[1]/2, "Player " + engine.firstPlace + " wins!")
    engine.window.addText(engine.dimensions[0]/2, engine.dimensions[1]/3, "Press 'q' to exit game")
    engine.window.addText(engine.dimensions[0]/2, engine.dimensions[1]/3, "Press 'r' to restart game")
    if userData == "quit":
        engine.status = "stopped"
    elif userData == "r":
        engine.cycle = "startup"

def quit_state(engine, state, userData):
    # Update game state
    # Do stuff
    # Add stuff to screen (Don't render. Happens in main loop)
    engine.window.clear()
    engine.window.fill((200, 200, 200))
    engine.window.addText(engine.dimensions[0]/2, engine.dimensions[1]/3, "Press 'q' to exit game")
    if userData == "quit":
        engine.status = "stopped"
