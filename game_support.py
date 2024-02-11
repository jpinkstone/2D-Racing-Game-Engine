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
    # engine.EngineActions.addPlayer()
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
