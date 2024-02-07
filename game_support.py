import pygame

# Game specific functions

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
    engine.screen.fill((200, 200, 200))
    engine.screen.addText(state.dimensions[0]/2, state.dimensions[1]/2, state.title)
    engine.screen.addText(state.dimensions[0]/2, state.dimensions[1]/3, "Press 'Enter' to begin game")
    if userData == "enter":
        state.cycle = "startup"

def startup_state(engine, state, userData):
    # Update game state
    # Do stuff
    # Add stuff to screen (Don't render. Happens in main loop)
    engine.screen.clear()
    engine.screen.addMap()
    engine.EngineActions.addPlayer()
    engine.audio.startMusic()
    engine.EngineActions.startGame()
    state.cycle = "game"

def game_state(engine, state, userData):
    # Update game state
    # Do stuff
    # Add stuff to screen (Don't render. Happens in main loop)
    engine.GameActions(userData)
    engine.physics()
    if state.timeLeft <= 0:
        state.cycle = "done"

def done_state(engine, state, userData):
    # Update game state
    # Do stuff
    # Add stuff to screen (Don't render. Happens in main loop)
    engine.screen.clear()
    engine.screen.fill((200, 200, 200))
    engine.screen.addText(state.dimensions[0]/2, state.dimensions[1]/2, "Player " + state.firstPlace + " wins!")
    engine.screen.addText(state.dimensions[0]/2, state.dimensions[1]/3, "Press 'q' to exit game")
    engine.screen.addText(state.dimensions[0]/2, state.dimensions[1]/3, "Press 'r' to restart game")
    if userData == "quit":
        state.status = "stopped"
    elif userData == "r":
        state.cycle = "startup"

def quit_state(engine, state, userData):
    # Update game state
    # Do stuff
    # Add stuff to screen (Don't render. Happens in main loop)
    engine.screen.clear()
    engine.screen.fill((200, 200, 200))
    engine.screen.addText(state.dimensions[0]/2, state.dimensions[1]/3, "Press 'q' to exit game")
    if userData == "quit":
        state.status = "stopped"
