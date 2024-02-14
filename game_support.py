from game_engine import *

def getInput():
    actions = []

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            actions.append(EVENT_QUIT)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                actions.append(EVENT_DECELF)
            if event.key == pygame.K_s:
                actions.append(EVENT_DECELB)
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        actions.append(EVENT_ACCELF)
    if keys[pygame.K_s]:
        actions.append(EVENT_ACCELB)
    if keys[pygame.K_a]:
        actions.append(EVENT_LEFT)
    if keys[pygame.K_d]:
        actions.append(EVENT_RIGHT)
    if keys[pygame.K_r]:
        actions.append(EVENT_RESTART)
    if keys[pygame.K_RETURN]:
        actions.append(EVENT_ENTER)
    if keys[pygame.K_q]:
        actions.append(EVENT_QUIT)

    return actions
            
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
    if "enter" in userData:
        state.cycle = "startup"
    elif "quit" in userData:
        state.status = "stopped"

def startup_state(engine, state, userData):
    # Update game state
    # Do stuff
    # Add stuff to screen (Don't render. Happens in main loop)
    clear(engine)
    player = PlayerGameState(state.playerId,500,500)
    EngineActions.addPlayer(state, player)
    audio.startMusic()
    EngineActions.setGameTime(state, 180)
    EngineActions.setLastTime(state, int(datetime.datetime.today().timestamp()))
    assets = ["track.png", "track_mask.png", "race_car0.png", "race_car1.png", "race_car2.png", "race_car3.png",]
    track, track_mask, car0, car1, car2, car3 = loadAssets(assets)
    state.cycle = "game"

def game_state(engine, state, userData):
    # Update game state
    # Do stuff
    # Add stuff to screen (Don't render. Happens in main loop)
    clear(engine)
    map_mask = addMap(engine, "track.png", "track_mask.png", state.dimensions)
    player_mask = addPlayer(engine, state.players[0], (state.players[0].width/8, state.players[0].height/8))
    GameActions().handle_actions(state, userData)
    addText(engine, state.dimensions[0]-125, 25, 'freesansbold.ttf', 32, "Time left: " + str(state.gameTime))
    getCollisions(map_mask, player_mask)
    if int(datetime.datetime.today().timestamp()) > state.lastTime:
        EngineActions.setLastTime(state, int(datetime.datetime.today().timestamp()))
        EngineActions.decreaseGameTime(state, 1)
    if state.gameTime <= 0:
        state.cycle = "done"
    if "quit" in userData:
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
    if "quit" in userData:
        state.status = "stopped"
    elif "r" in userData:
        state.cycle = "startup"

def quit_state(engine, state, userData):
    # Update game state
    # Do stuff
    # Add stuff to screen (Don't render. Happens in main loop)
    clear()
    fill((200, 200, 200))
    addText(engine, state.dimensions[0]/2, state.dimensions[1]/3, 'freesansbold.ttf', 32, "Press 'q' to exit game")
    if "quit" in userData:
        state.status = "stopped"
