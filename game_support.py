from game_engine import *

SPRITE_GREEN = "race_car2.png"
SPRITE_RED = "race_car0.png"
SPRITE_BLUE = "race_car3.png"
SPRITE_PINK = "race_car1.png"

Path = [
    (778, 689), (960, 686), (1158, 689), (1251, 672), 
    (1194, 576), (1130, 512), (1200, 455), (1286, 379), (1248, 334),
    (1149, 321), (1100, 259), (1156, 198), (1241, 157), (1276, 101),
    (1232, 63), (1149, 51), (887, 63), (644, 55), (507, 96),
    (502, 167), (636, 231), (816, 306), (967, 420), (969, 509),
    (864, 516), (722, 476), (558, 370), (389, 226), (235, 124),
    (167, 72), (120, 99), (101, 174), (124, 249), (200, 311),
    (270, 372), (261, 462), (160, 523), (127, 578), (155, 648),
    (226, 696), (379, 708), (558, 689)
]

def getInput():
    actions = []
    moved = False

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
        moved = True
    if keys[pygame.K_s]:
        actions.append(EVENT_ACCELB)
        moved = True
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

    if not moved:
        actions.append(EVENT_REDUCE_SPEED)
    return actions

def cycle(engine, state, userData):
    if state.cycle == "menu": menu_state(engine, state, userData)
    elif state.cycle == "game": game_state(engine, state, userData)
    elif state.cycle == "done": done_state(engine, state, userData)

def menu_state(engine, state, userData):
    engine.screenFill((200, 200, 200))
    engine.loadAssets(["splash.jpg"])
    engine.addSplash("splash.jpg", state.dimensions)
    engine.addText(state.dimensions[0]/2, state.dimensions[1]/1.35, "assets/paladins.ttf", 55, (255, 255, 255), "Tiny Turismo")
    if state.isServer:
        engine.addText(state.dimensions[0]/2, state.dimensions[1]/1.2, "assets/paladins.ttf", 20, (255, 255, 255), "You are the Server")
        engine.addText(state.dimensions[0]/2, state.dimensions[1]/1.25, "assets/paladins.ttf", 20, (255, 255, 255), "Press Enter to Start")
    else:
        engine.addText(state.dimensions[0]/2, state.dimensions[1]/1.2, "assets/paladins.ttf", 20, (255, 255, 255), "You are a client")
        engine.addText(state.dimensions[0]/2, state.dimensions[1]/1.25, "assets/paladins.ttf", 20, (255, 255, 255), "Waiting for Server to Start")
    engine.addText(state.dimensions[0]/2, state.dimensions[1]/1.1, "assets/paladins.ttf", 15, (255, 255, 255), "Connected Players: " + str(len(state.players)))
    engine.addText(state.dimensions[0]/2, state.dimensions[1]/1.07, "assets/paladins.ttf", 15, (255, 255, 255), "AI Players: " + str(3-len(state.players)))
    if EVENT_ENTER in userData and state.isServer:
        state.cycle = "game"
    elif EVENT_QUIT in userData:
        state.status = "stopped"
        print("Exiting...")

def game_state(engine, state, userData):
    if state.startup == False:
        player = PlayerGameState(60, 60)
        player.sprite_id = state.sprite_id
        engine.addPlayer(state, state.player_id, player)
        random.seed()
        if state.isServer:
            for x in range(4-len(state.players)):
                playerAI = PlayerAI(Path, random.uniform(0.1, 0.9), random.uniform(2, 5))
                playerAI.sprite_id = SPRITE_PINK
                playerAI.id = x+1
                engine.addPlayerAI(state, playerAI)
        audio.init()
        audio.startMusic()
        assets = ["track.png", "track_mask.png", "race_car0.png", "race_car1.png", "race_car2.png", "race_car3.png"]
        engine.loadAssets(assets)
        engine.setGameTime(state, 180)
        engine.setLastTime(state, int(datetime.datetime.today().timestamp()))
        state.startup = True

    engine.clear()
    map_mask = engine.addMap("track.png", "track_mask.png", state.dimensions)
    for id in state.players.keys():
        player_mask = engine.placePlayer(state.players[id], (state.players[id].dimensions[0], state.players[id].dimensions[1]))

    if engine.getCollisions(map_mask, state.players[state.player_id], player_mask, state):
            engine.bounce(state)
    engine.handle_actions(state, userData)
    
    for id in range(len(state.playersAI)):
        if id > 4 - len(state.players): break
        player_mask = engine.placePlayer(state.playersAI[id], (state.playersAI[id].dimensions[0], state.playersAI[id].dimensions[1]))
        if state.isServer:
            state.playersAI[id].follow_waypoints()

    engine.addText(state.dimensions[0]-200, 25, "assets/paladins.ttf", 17, (0, 0, 0), "Time left: " + str(state.gameTime))
    if int(datetime.datetime.today().timestamp()) > int(state.lastTime):
        engine.setLastTime(state, int(datetime.datetime.today().timestamp()))
        engine.decreaseGameTime(state, 1)
    if state.gameTime <= 0:
        state.cycle = "done"
    if EVENT_QUIT in userData:
        state.status = "stopped"
        print("Exiting...")

def done_state(engine, state, userData):
    engine.clear()
    engine.screenFill((200, 200, 200))
    engine.addText(state.dimensions[0]/2, state.dimensions[1]/3, "assets/paladins.ttf", 32, (0, 0, 0), "Player " + str(state.firstPlace) + " wins!")
    engine.addText(state.dimensions[0]/2, state.dimensions[1]/1.2, "assets/paladins.ttf", 20, (0, 0, 0), "Press 'q' to exit game")
    engine.addText(state.dimensions[0]/2, state.dimensions[1]/1.25, "assets/paladins.ttf", 20, (0, 0, 0), "Press 'r' to restart game")
    if EVENT_QUIT in userData:
        state.status = "stopped"
        print("Exiting...")
    elif EVENT_RESTART in userData:
        state.startup = False
        state.players.clear()
        state.playersAI.clear()
        state.cycle = "menu"
