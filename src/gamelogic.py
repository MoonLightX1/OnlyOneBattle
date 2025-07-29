import pygame

from stagedata import *
from wave_splash import *
from projectiles import *
from util import *
from player import *
from melee import Sword
from rockets import *
from boss import *
from theflappybird import *
from bg import *
from giantlazer import *
from spinningballs import *
from acidrain import *
from shield import Shield 
from dialouge import *

def mainmenu(screen, state):
    main_image = pygame.image.load("data/artwork/mainmenutemp.png")

    stage_mgr = StageManager()
    if stage_mgr.load_stage() == None:
        print("Stage not found, setting to default stage 1.")
        stage_mgr.save_stage(1)  # Ensure stage is set to 1 if not found
    print(f"Current stage: {stage_mgr.load_stage()}") #Testing stage loading

    # Prepare transition intro (fade-in)
    frame_paths = [
        "data/artwork/transitions/frame__0001.png",
        "data/artwork/transitions/frame__0002.png",
        "data/artwork/transitions/frame__0003.png",
        "data/artwork/transitions/frame__0004.png",
        "data/artwork/transitions/frame__0005.png",
        "data/artwork/transitions/frame__0006.png",
        "data/artwork/transitions/frame__0007.png",
        "data/artwork/transitions/frame__0008.png",
        "data/artwork/transitions/frame__0009.png",
        "data/artwork/transitions/frame__0010.png",
        "data/artwork/transitions/frame__0011.png",
        "data/artwork/transitions/frame__0012.png",
        "data/artwork/transitions/frame__0013.png",
        "data/artwork/transitions/frame__0014.png",
        "data/artwork/transitions/frame__0015.png",
        "data/artwork/transitions/frame__0016.png"
    ]

    # Create intro transition (reverse=False)
    intro_transition = TiledTransition(frame_paths, screen.get_size(), reverse=True)
    
    AudioLoop = SFX("data/sounds/tracks/title_loop.mp3")
    AudioLoop.play(1,1,True,0.5)

    # Run intro transition
    clock = pygame.time.Clock()
    while not intro_transition.is_done():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
        screen.blit(main_image, (0, 0))
        intro_transition.update()
        intro_transition.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    screen.blit(main_image, (0, 0))
    pygame.display.flip()

    # Wait time tracking
    leavinshi = False

    # Prepare outro transition (fade-out, reverse=True)
    outro_transition = TiledTransition(frame_paths, screen.get_size(), reverse=False)

    running = True
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    leavinshi = True

        if leavinshi:
            # Run outro transition
            if not outro_transition.is_done():
                screen.blit(main_image, (0, 0))
                outro_transition.update()
                outro_transition.draw(screen)
                pygame.display.flip()
            else:
                # After fade-out, change state
                state.change("fighting_dialog")
                AudioLoop.stop()
                return "stay"
        else:
            # Still waiting, just show main image
            screen.blit(main_image, (0, 0))

def deadscreen_logic(screen, state):
    main_image = pygame.image.load("data/artwork/deadscreen.png")

    # Prepare transition intro (fade-in)
    frame_paths = [
        "data/artwork/transitions/frame__0001.png",
        "data/artwork/transitions/frame__0002.png",
        "data/artwork/transitions/frame__0003.png",
        "data/artwork/transitions/frame__0004.png",
        "data/artwork/transitions/frame__0005.png",
        "data/artwork/transitions/frame__0006.png",
        "data/artwork/transitions/frame__0007.png",
        "data/artwork/transitions/frame__0008.png",
        "data/artwork/transitions/frame__0009.png",
        "data/artwork/transitions/frame__0010.png",
        "data/artwork/transitions/frame__0011.png",
        "data/artwork/transitions/frame__0012.png",
        "data/artwork/transitions/frame__0013.png",
        "data/artwork/transitions/frame__0014.png",
        "data/artwork/transitions/frame__0015.png",
        "data/artwork/transitions/frame__0016.png"
    ]
    frame_paths_other = [ #just to work with that like white flash yk
        "data/artwork/transitions/white_ver/frame__0001.png",
        "data/artwork/transitions/white_ver/frame__0002.png",
        "data/artwork/transitions/white_ver/frame__0003.png",
        "data/artwork/transitions/white_ver/frame__0004.png",
        "data/artwork/transitions/white_ver/frame__0005.png",
        "data/artwork/transitions/white_ver/frame__0006.png",
        "data/artwork/transitions/white_ver/frame__0007.png",
        "data/artwork/transitions/white_ver/frame__0008.png",
        "data/artwork/transitions/white_ver/frame__0009.png",
        "data/artwork/transitions/white_ver/frame__0010.png",
        "data/artwork/transitions/white_ver/frame__0011.png",
        "data/artwork/transitions/white_ver/frame__0012.png",
        "data/artwork/transitions/white_ver/frame__0013.png",
        "data/artwork/transitions/white_ver/frame__0014.png",
        "data/artwork/transitions/white_ver/frame__0015.png",
        "data/artwork/transitions/white_ver/frame__0016.png"
    ]

    # Create intro transition (reverse=False)
    intro_transition = TiledTransition(frame_paths_other, screen.get_size(), reverse=True)
    
    AudioLoop = SFX("data/sounds/tracks/game_over.mp3")
    AudioLoop.play(1,1,False,0.5)

    # Run intro transition
    clock = pygame.time.Clock()
    while not intro_transition.is_done():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
        screen.blit(main_image, (0, 0))
        intro_transition.update()
        intro_transition.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    screen.blit(main_image, (0, 0))
    pygame.display.flip()

    # Wait time tracking
    leavinshi = False

    # Prepare outro transition (fade-out, reverse=True)
    outro_transition = TiledTransition(frame_paths, screen.get_size(), reverse=False)

    running = True
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    leavinshi = True

        if leavinshi:
            # Run outro transition
            if not outro_transition.is_done():
                screen.blit(main_image, (0, 0))
                outro_transition.update()
                outro_transition.draw(screen)
                pygame.display.flip()
            else:
                # After fade-out, change state
                state.change("fighting_dialog")
                AudioLoop.stop()
                return "stay"
        else:
            # Still waiting, just show main image
            screen.blit(main_image, (0, 0))
            pygame.display.flip()

def fightingscreen_dialog_logic(screen, state):
    clock = pygame.time.Clock()

    # Load images once
    bg = pygame.image.load("data/artwork/battlingscreen_options.png")
    
    stage_mgr = StageManager()
    if stage_mgr.load_stage() == None:
        print("Stage not found, setting to default stage 1.")
        stage_mgr.save_stage(1)  # Ensure stage is set to 1 if not found
    print(f"Current stage: {stage_mgr.load_stage()}") #Testing stage loading
    
    buttonSFX = SFX("data/sounds/swap item sfx.mp3")
    changeSFX = SFX("data/sounds/button hover sfx.mp3")

    buttons = [
        Button("ATTACK", 28, 27, "data/artwork/attack.png", 601, 232),
        Button("TALK", 674, 27, "data/artwork/talk.png", 601, 232),
        Button("CRY", 1304, 27, "data/artwork/mock.png", 601, 232), #just ref as cry if have time i can change to mock
    ]
    my_font = pygame.font.Font("data/fonts/vcrosdneue.ttf", 30)
    dialogue_manager = DialogueManager(font=my_font, screen=screen)

    pygame.mixer.init()
    word_sound = pygame.mixer.Sound("data/sounds/voice.WAV")

    frames = [f"data/artwork/transitions/frame__{str(i).zfill(4)}.png" for i in range(1, 17)]

    # Play intro transition first
    intro_transition = TiledTransition(frames, screen.get_size(), reverse=True)
    while not intro_transition.is_done():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

        screen.blit(bg, (0, 0))

        for button in buttons:
            screen.blit(button.icon, (button.x, button.y))

        intro_transition.update()
        intro_transition.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    scaled_up_button_index = None
    last_clicked_button_index = None
    show_dialogbox_example = False
    
    Music = SFX("data/sounds/tracks/idletension.mp3")
    Music.play(1,1,True,0.5)

    isindialouge = False
    enter_pressed_time = None
    outro_transition = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                for i, button in enumerate(buttons):
                    if button.is_clicked(mouse_pos):
                        changeSFX.play(0.6,1.5,False,0.5)
                        last_clicked_button_index = i
                        scaled_up_button_index = i
                        show_dialogbox_example = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and last_clicked_button_index == 0 and not show_dialogbox_example and isindialouge == False: #0 is attack
                    buttonSFX.play(0.6,1.5,False,0.4)
                    show_dialogbox_example = True
                    dialogue_manager.queue_dialogue("This is what YOU wanted.", "AMALGAM", type_time=2, stay_time=1, char_sound=word_sound, pitch_factor=0.8)
                    enter_pressed_time = pygame.time.get_ticks()  # start delay timer
                if stage_mgr.load_stage() == 1:
                    if event.key == pygame.K_RETURN and last_clicked_button_index == 1 and isindialouge == False and not show_dialogbox_example: #1 is talk
                        buttonSFX.play(0.6,1.5,False,0.4)
                        isindialouge = True
                        dialogue_manager.queue_dialogue("...", "AMALGAM", type_time=1, stay_time=2, char_sound=word_sound, pitch_factor=0.8)
                        delayed_call(3, lambda: dialogue_manager.queue_dialogue("Who are you?", "MC", type_time=2, stay_time=2, char_sound=word_sound, pitch_factor=0.6))
                        delayed_call(7, lambda: dialogue_manager.queue_dialogue("...", "AMALGAM", type_time=1, stay_time=2, char_sound=word_sound, pitch_factor=0.8))
                        delayed_call(10, lambda: dialogue_manager.queue_dialogue("What are you?", "MC", type_time=2, stay_time=2, char_sound=word_sound, pitch_factor=0.6))
                        delayed_call(14, lambda: dialogue_manager.queue_dialogue("...", "AMALGAM", type_time=1, stay_time=2, char_sound=word_sound, pitch_factor=0.8))
                        delayed_call(17, lambda: dialogue_manager.queue_dialogue("Okay", "MC", type_time=2, stay_time=2, char_sound=word_sound, pitch_factor=0.6))
                        def end_dialogue():
                            nonlocal isindialouge
                            isindialouge = False
                        delayed_call(21, end_dialogue)
                    if event.key == pygame.K_RETURN and last_clicked_button_index == 2 and isindialouge == False and not show_dialogbox_example: #2 is mock
                        buttonSFX.play(0.6,1.5,False,0.4)
                        isindialouge = True
                        dialogue_manager.queue_dialogue("Hmph, I guess I shouldn't mock them..", "MC", type_time=2, stay_time=2, char_sound=word_sound, pitch_factor=0.6)
                        def end_dialogue():
                            nonlocal isindialouge
                            isindialouge = False
                        delayed_call(4, end_dialogue)
                elif stage_mgr.load_stage() == 2:
                    if event.key == pygame.K_RETURN and last_clicked_button_index == 1 and isindialouge == False and not show_dialogbox_example: #1 is talk
                        buttonSFX.play(0.6,1.5,False,0.4)
                        isindialouge = True
                        dialogue_manager.queue_dialogue("I don't want to hurt you. Please stop attacking me.", "MC", type_time=2, stay_time=2, char_sound=word_sound, pitch_factor=0.6)
                        delayed_call(4, lambda: dialogue_manager.queue_dialogue("No.", "AMALGAM", type_time=2, stay_time=2, char_sound=word_sound, pitch_factor=0.8))
                        delayed_call(8, lambda: dialogue_manager.queue_dialogue("No?", "MC", type_time=1, stay_time=2, char_sound=word_sound, pitch_factor=0.6))
                        delayed_call(11, lambda: dialogue_manager.queue_dialogue("No.", "AMALGAM", type_time=1, stay_time=2, char_sound=word_sound, pitch_factor=0.8))
                        delayed_call(14, lambda: dialogue_manager.queue_dialogue("Can you say anything besides no?", "MC", type_time=2, stay_time=2, char_sound=word_sound, pitch_factor=0.6))
                        delayed_call(18, lambda: dialogue_manager.queue_dialogue("Yes.", "AMALGAM", type_time=1, stay_time=2, char_sound=word_sound, pitch_factor=0.8))
                        delayed_call(21, lambda: dialogue_manager.queue_dialogue("Okay... then... how've you been?", "MC", type_time=2, stay_time=2, char_sound=word_sound, pitch_factor=0.6))
                        delayed_call(25, lambda: dialogue_manager.queue_dialogue("I’ve been. I’ve been for a while, how though? You already know.", "AMALGAM", type_time=2, stay_time=2, char_sound=word_sound, pitch_factor=0.8))
                        delayed_call(29, lambda: dialogue_manager.queue_dialogue("What?", "MC", type_time=1, stay_time=2, char_sound=word_sound, pitch_factor=0.6))
                        delayed_call(32, lambda: dialogue_manager.queue_dialogue("I still think about the smell of his shampoo when I’m alone.", "AMALGAM", type_time=3, stay_time=2, char_sound=word_sound, pitch_factor=0.8))
                        def end_dialogue():
                            nonlocal isindialouge
                            isindialouge = False
                            stage_mgr.save_stage(7) #To save they talked.
                        delayed_call(37, end_dialogue)
                    if event.key == pygame.K_RETURN and last_clicked_button_index == 2 and isindialouge == False and not show_dialogbox_example: #2 is mock
                        buttonSFX.play(0.6,1.5,False,0.4)
                        isindialouge = True
                        dialogue_manager.queue_dialogue("You're an ugly bastard aren't you?", "MC", type_time=2, stay_time=2, char_sound=word_sound, pitch_factor=0.6)
                        delayed_call(4, lambda: dialogue_manager.queue_dialogue("...", "AMALGAM", type_time=1, stay_time=2, char_sound=word_sound, pitch_factor=0.8))
                        delayed_call(7, lambda: dialogue_manager.queue_dialogue("Do me a favor and die already, make it snappy.", "MC", type_time=2, stay_time=2, char_sound=word_sound, pitch_factor=0.6))
                        delayed_call(11, lambda: dialogue_manager.queue_dialogue("No.", "AMALGAM", type_time=1, stay_time=2, char_sound=word_sound, pitch_factor=0.8))
                        delayed_call(14, lambda: dialogue_manager.queue_dialogue("So it speaks...", "MC", type_time=1.5, stay_time=2, char_sound=word_sound, pitch_factor=0.6))
                        delayed_call(17.5, lambda: dialogue_manager.queue_dialogue("You've recieve a shield! Press F to activate it for 20 seconds with a delay of 10.", "???", type_time=3, stay_time=2, char_sound=word_sound, pitch_factor=1.5))
                        def end_dialogue():
                            nonlocal isindialouge
                            isindialouge = False
                            stage_mgr.save_stage(8) #To give the shield.
                        delayed_call(22.5, end_dialogue)
                elif stage_mgr.load_stage() == 4: # Stage 4 is they talked
                    if event.key == pygame.K_RETURN and last_clicked_button_index == 1 and isindialouge == False and not show_dialogbox_example: #1 is talk
                        buttonSFX.play(0.6,1.5,False,0.4)
                        isindialouge = True
                        dialogue_manager.queue_dialogue("I don't want to hurt you. Please stop attacking me.", "MC", type_time=2, stay_time=2, char_sound=word_sound, pitch_factor=0.6)
                        delayed_call(4, lambda: dialogue_manager.queue_dialogue("My food, my consumption, my existence requires.", "AMALGAM", type_time=2, stay_time=2, char_sound=word_sound, pitch_factor=0.8))
                        delayed_call(8, lambda: dialogue_manager.queue_dialogue("So you’re hungry?", "MC", type_time=1, stay_time=2, char_sound=word_sound, pitch_factor=0.6))
                        delayed_call(11, lambda: dialogue_manager.queue_dialogue("With you I’m always full. When you’re alone with your thoughts I am most powerful,", "AMALGAM", type_time=2, stay_time=2, char_sound=word_sound, pitch_factor=0.8))
                        delayed_call(15, lambda: dialogue_manager.queue_dialogue("when you hold up his picture frame, I am most present.", "AMALGAM", type_time=2, stay_time=2, char_sound=word_sound, pitch_factor=0.8))
                        delayed_call(20, lambda: dialogue_manager.queue_dialogue("He wouldn’t like you.", "MC", type_time=1.5, stay_time=2, char_sound=word_sound, pitch_factor=0.6))
                        delayed_call(23.5, lambda: dialogue_manager.queue_dialogue("But he’d understand.", "AMALGAM", type_time=1.5, stay_time=2, char_sound=word_sound, pitch_factor=0.8))
                        delayed_call(27, lambda: dialogue_manager.queue_dialogue("Well, I think I know what you are. How’ve you been?", "MC", type_time=2, stay_time=2, char_sound=word_sound, pitch_factor=0.6))
                        delayed_call(31, lambda: dialogue_manager.queue_dialogue("I’ve been. I’ve been for a while, how though? You already know.", "AMALGAM", type_time=2, stay_time=2, char_sound=word_sound, pitch_factor=0.8))
                        delayed_call(35, lambda: dialogue_manager.queue_dialogue("What?", "MC", type_time=1, stay_time=2, char_sound=word_sound, pitch_factor=0.6))
                        delayed_call(39, lambda: dialogue_manager.queue_dialogue("I still think about the smell of his shampoo when I’m alone.", "AMALGAM", type_time=3, stay_time=2, char_sound=word_sound, pitch_factor=0.8))
                        delayed_call(43, lambda: dialogue_manager.queue_dialogue("I think I had a cat once, a lanky tabby with a nasty attitude. Nepenthe. I grew up- ", "MC", type_time=2, stay_time=2, char_sound=word_sound, pitch_factor=0.6))
                        delayed_call(47, lambda: dialogue_manager.queue_dialogue("with him since we were born the same month. I remember he was afraid of me since I’d ", "MC", type_time=2, stay_time=2, char_sound=word_sound, pitch_factor=0.6))
                        delayed_call(51, lambda: dialogue_manager.queue_dialogue("chase him around and roughhouse. I know that’s bad, but I was an unattended child. ", "MC", type_time=2, stay_time=2, char_sound=word_sound, pitch_factor=0.6))
                        delayed_call(55, lambda: dialogue_manager.queue_dialogue("An unattended child is gonna terrorize some poor animal. Things got better when I", "MC", type_time=2, stay_time=2, char_sound=word_sound, pitch_factor=0.6))
                        delayed_call(58, lambda: dialogue_manager.queue_dialogue("got older. I’d clean his poo and puke, I think that made up for the terror. We’d", "MC", type_time=2, stay_time=2, char_sound=word_sound, pitch_factor=0.6))
                        delayed_call(62, lambda: dialogue_manager.queue_dialogue("cuddle as we watched TV and sometimes we’d watch the street from the windowsill", "MC", type_time=2, stay_time=2, char_sound=word_sound, pitch_factor=0.6))
                        delayed_call(66, lambda: dialogue_manager.queue_dialogue("together … . I miss him.", "MC", type_time=2, stay_time=2, char_sound=word_sound, pitch_factor=0.6))
                        delayed_call(70, lambda: dialogue_manager.queue_dialogue("I miss Nepenthe as much as you do. But not as much as him.", "AMALGAM", type_time=2, stay_time=2, char_sound=word_sound, pitch_factor=0.8))
                        delayed_call(74, lambda: dialogue_manager.queue_dialogue("I know.", "MC", type_time=1, stay_time=2, char_sound=word_sound, pitch_factor=0.6))
                        def end_dialogue():
                            nonlocal isindialouge
                            isindialouge = False
                        delayed_call(77, end_dialogue)
                    if event.key == pygame.K_RETURN and last_clicked_button_index == 2 and isindialouge == False and not show_dialogbox_example:
                        buttonSFX.play(0.6,1.5,False,0.4)
                        isindialouge = True
                        dialogue_manager.queue_dialogue("Hmph mocking him will only make the situation worse.", "MC", type_time=3, stay_time=2, char_sound=word_sound, pitch_factor=0.6)
                        def end_dialogue():
                            nonlocal isindialouge
                            isindialouge = False
                elif stage_mgr.load_stage() == 5: #5 = they mocked b4
                    if event.key == pygame.K_RETURN and last_clicked_button_index == 1 and isindialouge == False and not show_dialogbox_example:
                        buttonSFX.play(0.6,1.5,False,0.4)
                        isindialouge = True
                        dialogue_manager.queue_dialogue("What's the point in talking to this loser anyway?", "MC", type_time=3, stay_time=2, char_sound=word_sound, pitch_factor=0.6)
                        def end_dialogue():
                            nonlocal isindialouge
                            isindialouge = False
                        delayed_call(2, end_dialogue)
                    if event.key == pygame.K_RETURN and last_clicked_button_index == 2 and isindialouge == False and not show_dialogbox_example: #2 is mock
                        buttonSFX.play(0.6,1.5,False,0.4)
                        isindialouge = True
                        dialogue_manager.queue_dialogue("Awww, is someone dying? Are you in pain?", "MC", type_time=2, stay_time=2, char_sound=word_sound, pitch_factor=0.6)
                        delayed_call(4, lambda: dialogue_manager.queue_dialogue("...", "AMALGAM", type_time=1, stay_time=2, char_sound=word_sound, pitch_factor=0.8))
                        delayed_call(7, lambda: dialogue_manager.queue_dialogue("I know why you’re here. You’re tired of it all. You want me to kill you.", "MC", type_time=2, stay_time=2, char_sound=word_sound, pitch_factor=0.6))
                        delayed_call(11, lambda: dialogue_manager.queue_dialogue("Please.", "AMALGAM", type_time=1, stay_time=2, char_sound=word_sound, pitch_factor=0.8))
                        delayed_call(14, lambda: dialogue_manager.queue_dialogue("Pathetic", "MC", type_time=1, stay_time=2, char_sound=word_sound, pitch_factor=0.6))
                        delayed_call(17, lambda: dialogue_manager.queue_dialogue("It would be a blessing.", "AMALGAM", type_time=2, stay_time=2, char_sound=word_sound, pitch_factor=0.8))
                        delayed_call(21, lambda: dialogue_manager.queue_dialogue("No blessing came to him. I saw you over his body. You caused it.", "MC", type_time=2, stay_time=2, char_sound=word_sound, pitch_factor=0.6))
                        delayed_call(25, lambda: dialogue_manager.queue_dialogue("I did't-", "AMALGAM", type_time=2, stay_time=0, char_sound=word_sound, pitch_factor=0.8))
                        delayed_call(27, lambda: dialogue_manager.queue_dialogue("I DON’T BELIEVE YOU! I think you’re pathetic. Worthless. Just a", "MC", type_time=3, stay_time=2, char_sound=word_sound, pitch_factor=0.6))
                        delayed_call(32, lambda: dialogue_manager.queue_dialogue("fucking road block. Just die and leave my life already!", "MC", type_time=3, stay_time=2, char_sound=word_sound, pitch_factor=0.6))
                        delayed_call(38, lambda: dialogue_manager.queue_dialogue("I will never die.", "AMALGAM", type_time=1, stay_time=2, char_sound=word_sound, pitch_factor=0.8))
                        delayed_call(41, lambda: dialogue_manager.queue_dialogue("You're not immortal. I will kill you.", "MC", type_time=1, stay_time=2, char_sound=word_sound, pitch_factor=0.6))
                        delayed_call(44, lambda: dialogue_manager.queue_dialogue("I will only die when you die. When your last breath is taken.", "AMALGAM", type_time=3, stay_time=2, char_sound=word_sound, pitch_factor=0.8))
                        delayed_call(47, lambda: dialogue_manager.queue_dialogue("When your memory has been wiped. I will be a hole in your heart.", "AMALGAM", type_time=3, stay_time=2, char_sound=word_sound, pitch_factor=0.8))
                        delayed_call(52, lambda: dialogue_manager.queue_dialogue("A dagger in your back. A needle in your veins.", "AMALGAM", type_time=3, stay_time=2, char_sound=word_sound, pitch_factor=0.8))
                        delayed_call(57, lambda: dialogue_manager.queue_dialogue("You're dead...", "MC", type_time=1, stay_time=2, char_sound=word_sound, pitch_factor=0.6))
                        def end_dialogue():
                            nonlocal isindialouge
                            isindialouge = False
                        delayed_call(60, end_dialogue)
                elif stage_mgr.load_stage() == 7 or stage_mgr.load_stage() == 8 or stage_mgr.load_stage() == 3: #4/5/3
                    if event.key == pygame.K_RETURN and last_clicked_button_index == 1 and isindialouge == False and not show_dialogbox_example:
                        buttonSFX.play(0.6,1.5,False,0.4)
                        isindialouge = True
                        dialogue_manager.queue_dialogue("What's the point...", "MC", type_time=3, stay_time=2, char_sound=word_sound, pitch_factor=0.6)
                        def end_dialogue():
                            nonlocal isindialouge
                            isindialouge = False
                        delayed_call(5, end_dialogue)
                    if event.key == pygame.K_RETURN and last_clicked_button_index == 2 and isindialouge == False and not show_dialogbox_example: #2 is mock
                        buttonSFX.play(0.6,1.5,False,0.4)
                        isindialouge = True
                        dialogue_manager.queue_dialogue("What's the point...", "MC", type_time=3, stay_time=2, char_sound=word_sound, pitch_factor=0.6)
                        def end_dialogue():
                            nonlocal isindialouge
                            isindialouge = False
                        delayed_call(5, end_dialogue)

        screen.blit(bg, (0, 0))

        for i, button in enumerate(buttons):
            if i == scaled_up_button_index:
                enlarged = pygame.transform.scale(button.icon, (button.width + 30, button.height + 30))
                screen.blit(enlarged, (button.x - 15, button.y - 15))
            else:
                screen.blit(button.icon, (button.x, button.y))

        if show_dialogbox_example:
            # After 3 seconds, start outro if not started yet
            if enter_pressed_time and outro_transition is None:
                if pygame.time.get_ticks() - enter_pressed_time >= 3000:
                    outro_transition = TiledTransition(frames, screen.get_size(), reverse=False)

            # If outro started, update and draw it
            if outro_transition:
                outro_transition.update()
                outro_transition.draw(screen)
                if outro_transition.is_done():
                    Music.stop()
                    return "battlescreen_01"
        
        dialogue_manager.update()
        dialogue_manager.draw()

        pygame.display.flip()
        clock.tick(60)
    
def battle_screen_01(screen, state):
    global countdown_started, countdown_start_time
    global time_left_minutes, minutes_left, seconds_left
    countdown_started = False
    countdown_start_time = 0
    countdown_duration = 2 * 60 * 1000  # 2 minutes in ms
    time_left_minutes = 2.0
    minutes_left = 2
    seconds_left = 0
    clock = pygame.time.Clock()
    background = pygame.image.load("data/artwork/battlegroundbase.png")
    arena_bg = GlitchyArena("data/artwork/arena.png", (401, 624))
    arena_rect = pygame.Rect(401, 624, 1045, 456)
    player = Player(arena_rect.centerx - 25, arena_rect.bottom - 50, 50, 50, arena_rect)
    
    battlesong = SFX("data/sounds/tracks/battle_loop.mp3")
    battlesong_active = False
    
    current_weapon = "bullet" 
    sword = Sword(player, hitbox_size=1.2, damage=15, cooldown=0.4)
    
        # boss teheee
    boss = Boss("data/artwork/enemies_heart.png", x=1270, y=838, width=149, height=140, arena_rect=arena_rect)

    # Define wall outlines for collision, not the inner black arena
    wall_thickness = 8
    walls = [
        pygame.Rect(arena_rect.left, arena_rect.top, arena_rect.width, wall_thickness),  # top
        pygame.Rect(arena_rect.left, arena_rect.bottom - wall_thickness, arena_rect.width, wall_thickness),  # bottom
        pygame.Rect(arena_rect.left, arena_rect.top, wall_thickness, arena_rect.height),  # left
        pygame.Rect(arena_rect.right - wall_thickness, arena_rect.top, wall_thickness, arena_rect.height),  # right
    ]
    
    #this is the stupidest shit ive coded wtf
    bossArry = [
        boss
    ]
    
    # attacks :3 :D :D ;D ;d :P i am not geting paid for this :sob:
    wave_splash_list = []
    flappybirds = []
    spinning_balls = []
    giant_lazers = []
    active_rocket_attacks = []
    acid_attack = None
    
    font = pygame.font.Font("data/fonts/vcrosdneue.ttf", 30)  # 30pt size
    
    boss_attack_timer = 0
    attack_interval = 95 # milliseconds / 95 for first, 120 for second, 120 for the third
    last_boss_attack = None 
    
    shield = None
    shield_active = False
    
    repressendingpotential = True
    
    switchitemSFX = SFX("data/sounds/swap item sfx.mp3")
    
    vfx_list = []
    
    throw_amount = 5
    
    stage_mgr = StageManager()
    if stage_mgr.load_stage() == None:
        print("Stage not found, setting to default stage 1.")
        stage_mgr.save_stage(1)  # Ensure stage is set to 1 if not found
    print(f"Current stage: {stage_mgr.load_stage()}") #Testing stage loading
    
    if stage_mgr.load_stage() == 1:
        boss.health = 300
    elif stage_mgr.load_stage() == 2 or stage_mgr.load_stage() == 7 or stage_mgr.load_stage() == 8:
        boss.health = 200
    elif stage_mgr.load_stage() == 3 or stage_mgr.load_stage() == 4 or stage_mgr.load_stage() == 5:
        boss.health = 100

    # Transition intro
    transition = TiledTransition([
        "data/artwork/transitions/frame__0001.png",
        "data/artwork/transitions/frame__0002.png",
        "data/artwork/transitions/frame__0003.png",
        "data/artwork/transitions/frame__0004.png",
        "data/artwork/transitions/frame__0005.png",
        "data/artwork/transitions/frame__0006.png",
        "data/artwork/transitions/frame__0007.png",
        "data/artwork/transitions/frame__0008.png",
        "data/artwork/transitions/frame__0009.png",
        "data/artwork/transitions/frame__0010.png",
        "data/artwork/transitions/frame__0011.png",
        "data/artwork/transitions/frame__0012.png",
        "data/artwork/transitions/frame__0013.png",
        "data/artwork/transitions/frame__0014.png",
        "data/artwork/transitions/frame__0015.png",
        "data/artwork/transitions/frame__0016.png"
    ], screen.get_size(), reverse=True)

    # Intro display setup
    intro_display = True
    intro_start_time = pygame.time.get_ticks()
    intro_total_duration = 10000  # 10 seconds
    intro_flash_duration = 6000   # Flashing for 6 seconds, then fade for 4 seconds
    font_large = pygame.font.Font("data/fonts/vcrosdneue.ttf", 72)

    lvlcomplete = SFX("data/sounds/level completed.mp3")
    shootSFX = SFX("data/sounds/shoot sfx.mp3")
    rocketSFX = SFX("data/sounds/rocket sfx.mp3")
    limbsfx = SFX("data/sounds/limb sfx.mp3")
    heartpumpySFX = SFX("data/sounds/heart pump sfx.mp3") #heh funny name
    acidrainSFX = SFX("data/sounds/acid rain sfx.mp3")

    while not transition.is_done():
        screen.blit(background, (0, 0))
        pygame.draw.rect(screen, (0, 0, 0), arena_rect)
        for wall in walls:
            pygame.draw.rect(screen, (100, 100, 100), wall)
        transition.update()
        transition.draw(screen)
        pygame.display.flip()
        clock.tick(60)
    
    running = True
    while running:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.jump()
                elif event.key == pygame.K_1:
                    current_weapon = "bullet"
                    switchitemSFX.play(0.6,1.5,False,0.8)
                elif event.key == pygame.K_2:
                    current_weapon = "sword"
                    switchitemSFX.play(0.6,1.5,False,0.8)
                elif event.key == pygame.K_3:
                    current_weapon = "throwable"
                    switchitemSFX.play(0.6,1.5,False,0.8)
                elif event.key == pygame.K_f and not shield_active and (stage_mgr.load_stage() == 5 or stage_mgr.load_stage() == 8):
                    if shield is None:
                        shield = Shield(player)
                    if shield.is_ready():
                        shield.activate()
                        switchitemSFX.play(0.6,1.5,False,0.4)
                        current_weapon = None
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not shield_active:
                    if current_weapon == "bullet":
                        player.start_charging()
                    elif current_weapon == "sword":
                        sword.attack()
                    elif current_weapon == "throwable":
                        try:
                            if throwable.iscooldowndone == True:
                                if throw_amount != 0:
                                    shootSFX.play(0.8,1.8,False,1)
                                    throwable.subtract_amount(1)
                                    repressendingpotential = False
                                    mouse_x, mouse_y = pygame.mouse.get_pos()
                                    player_center_x = player.rect.centerx
                                    player_center_y = player.rect.centery
                                    throwable = Throwable(player_center_x, player_center_y, mouse_x, mouse_y)
                                    vfx_list.append(throwable)
                                    throwable.iscooldowndone = False
                                    throw_amount -= 1
                                    print(throw_amount)
                                    delayed_call(1.75, lambda: setattr(throwable, 'iscooldowndone', True))  # Cooldown for throwabl
                                else:
                                    print("Throwable amount is zero, cannot throw more.")
                            else:
                                print("Throwable is on cooldown, wait for it to be ready.")
                        except:
                            print("Throwable not initialized")
                            mouse_x, mouse_y = pygame.mouse.get_pos()
                            player_center_x = player.rect.centerx
                            player_center_y = player.rect.centery
                            throwable = Throwable(player_center_x, player_center_y, mouse_x, mouse_y)
                            vfx_list.append(throwable)
                            throwable.iscooldowndone = False
                            throw_amount -= 1
                            print(throw_amount)
                            delayed_call(1.75, lambda: setattr(throwable, 'iscooldowndone', True))  # Cooldown for throwabl    
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if not shield_active:
                    if current_weapon == "bullet":
                        player.stop_charging_and_shoot(vfx_list)
        if not intro_display:
            if stage_mgr.load_stage() == 1 or stage_mgr.load_stage():    #STAGE 1 ATTACKS WOOO
                if boss_attack_timer == attack_interval:
                    possible_actions_other = [1, 2, 3]
                    if last_boss_attack == 1:
                        possible_actions_other.remove(1)  # Remove Wave Splash if last used
                    action_other = random.choice(possible_actions_other)
                    last_boss_attack = action_other
                    print(f"[boss_attack_loop] Action chosen: {action_other}")
                    if action_other == 1:
                        print("Boss uses: Wave Splash")
                        splash_width = 20
                        gap = 6
                        spacing = splash_width + gap  # 26 px between start of one splash to next

                        for height_rank in range(8):
                            splash_x = 1240 + height_rank * spacing
                            limbsfx.play(0.6,1.5,False,0.5)
                            wave_splash_list.append(WaveSplashRect(splash_x, arena_rect, height_rank, width=splash_width))
                    elif action_other == 2:
                        print("Boss uses: Flappy Birf")
                        limbsfx.play(0.6,1.5,False,0.5)
                        flappybirds.append(
                                FlappyBird(x=1266, arena_rect=arena_rect)
                            )
                    elif action_other == 3:
                        print("Boss uses: Spinning Balls")
                        angles = [i for i in range(30, 360, 30)] 
                        for angle in angles:
                            rad = math.radians(angle)
                            speed = 5
                            dx = math.cos(rad) * speed
                            dy = math.sin(rad) * speed
                            spawn_x = boss.rect.centerx
                            spawn_y = boss.rect.centery
                            spinning_ball = SpinningBall(spawn_x, spawn_y, dx, dy, arena_rect)
                            vfx_list.append(spinning_ball)
                    boss_attack_timer = 0
                else:
                    boss_attack_timer += 1
            if stage_mgr.load_stage() == 2 or stage_mgr.load_stage() == 7 or stage_mgr.load_stage() == 8:     #STAGE 2 ATTACKS WOOOO
                if boss_attack_timer == attack_interval:
                    possible_actions = [1, 2, 3, 4 ,5] # Rockets are more rare
                    if last_boss_attack == 1:
                        possible_actions.remove(1)  # Remove Acid Rain if last used
                    action = random.choice(possible_actions)
                    last_boss_attack = action
                    print(f"[boss_attack_loop] Action chosen: {action}")
                    if action == 1 or action == 4:
                        print("Boss uses: ACID RAIN :scary:")
                        acidrainSFX.play(0.6,1.5,False,0.9)
                        acid_attack = AcidRainAttack(arena_rect, player)
                    elif action == 2 or action == 5:
                        print("Boss uses: GYANT LAZER")
                        giant_lazers.append(GiantLazer(boss, arena_rect))
                    elif action == 3:
                        print("Boss uses: rocket lazer :sad:")
                        rocketSFX.play(0.6,1.5,False,0.8)
                        new_attack = RocketsAttack(boss, player, arena_rect)
                        active_rocket_attacks.append(new_attack)
                    boss_attack_timer = 0
                else:
                    boss_attack_timer += 1
            if stage_mgr.load_stage() == 3 or stage_mgr.load_stage() == 4 or stage_mgr.load_stage() == 5:    #STAGE 3 ATTACKS WOOO
                if boss_attack_timer == attack_interval:
                    possible_actions_other = [1, 2, 3, 4]
                    try:
                        if last_boss_attack == 1 or last_boss_attack == 4:
                            possible_actions_other.remove(1) 
                    except NameError:
                        print("last_boss_attack not defined, using default actions.")
                    action_other = random.choice(possible_actions_other)
                    last_boss_attack = action_other
                    print(f"[boss_attack_loop] Action chosen: {action_other}")
                    if action_other == 1:
                        print("Boss uses: Wave Splash")
                        splash_width = 20
                        gap = 6
                        spacing = splash_width + gap  # 26 px between start of one splash to next
                        for height_rank in range(8):
                            splash_x = 1240 + height_rank * spacing
                            limbsfx.play(0.6,1.5,False,0.5)
                            wave_splash_list.append(WaveSplashRect(splash_x, arena_rect, height_rank, width=splash_width))
                    elif action_other == 2:
                        print("Boss uses: Spinning Balls")
                        angles = [i for i in range(30, 360, 30)]
                        for angle in angles:
                            rad = math.radians(angle)
                            speed = 5
                            dx = math.cos(rad) * speed
                            dy = math.sin(rad) * speed
                            spawn_x = boss.rect.centerx
                            spawn_y = boss.rect.centery
                            spinning_ball = SpinningBall(spawn_x, spawn_y, dx, dy, arena_rect)
                            vfx_list.append(spinning_ball)
                    if action_other == 3:
                        print("Boss uses: ACID RAIN :scary:")
                        acidrainSFX.play(0.6,1.5,False,0.9)
                        acid_attack = AcidRainAttack(arena_rect, player)
                    elif action_other == 4:
                        print("Boss uses: GYANT LAZER")
                        giant_lazers.append(GiantLazer(boss, arena_rect))
                    boss_attack_timer = 0
                else:
                    boss_attack_timer += 1
                    
        if not battlesong_active:
            battlesong.play(1,1,True, 0.5)
            battlesong_active = True
        player.update(keys, walls, vfx_list)
        player.handle_reload()
        # Remove done VFX and dead bullets
        vfx_list = [v for v in vfx_list if (not isinstance(v, Bullet) or v.alive) and not getattr(v, "is_done", lambda: False)()]

        if boss.health < 100 and stage_mgr.load_stage() == 3 or stage_mgr.load_stage() == 4 or stage_mgr.load_stage() == 5 and repressendingpotential == True:
            repressendingpotential = False #Just an easy way to do it lol
            print("No longer capable of doing RepressEnding!")

        screen.blit(background, (0, 0))
        arena_bg.update()
        arena_bg.draw(screen)
        # Boss intro warning text
        if intro_display:
            elapsed = pygame.time.get_ticks() - intro_start_time
            if elapsed >= intro_total_duration:
                intro_display = False
                heartpumpySFX.play(0.6,1.5,True,0.9)
            else:
                warning_text = font_large.render("! BOSS INCOMING !", True, (255, 140, 0))
                warning_surface = warning_text.convert_alpha()
                
                if elapsed <= intro_flash_duration:
                    # Flash every 500ms
                    flash_on = (elapsed // 500) % 2 == 0
                    if flash_on:
                        screen.blit(warning_surface, (
                            arena_rect.centerx - warning_surface.get_width() // 2,
                            arena_rect.centery - warning_surface.get_height() // 2
                        ))
                else:
                    # Fade out over last 4 seconds (4000ms)
                    fade_elapsed = elapsed - intro_flash_duration
                    fade_duration = intro_total_duration - intro_flash_duration
                    fade_ratio = 1.0 - (fade_elapsed / fade_duration)
                    alpha = int(255 * fade_ratio)
                    warning_surface.set_alpha(alpha)
                    screen.blit(warning_surface, (
                        arena_rect.centerx - warning_surface.get_width() // 2,
                        arena_rect.centery - warning_surface.get_height() // 2
                    ))

        if stage_mgr.load_stage() in (3, 4, 5):
            if not countdown_started:
                countdown_start_time = pygame.time.get_ticks()
                countdown_started = True
            else:
                time_passed = pygame.time.get_ticks() - countdown_start_time
                time_left_ms = max(0, countdown_duration - time_passed)

                time_left_minutes = time_left_ms / 60000  # float like 1.5 = 1m 30s
                minutes_left = int(time_left_ms / 60000)
                seconds_left = int((time_left_ms % 60000) / 1000)

                if time_passed >= countdown_duration:
                    print("Time is up pal")
                    if boss.health < 0:
                        print("Save Ending, boss not defeated")
                        battlesong.stop()
                        heartpumpySFX.stop()
                        return "mainmenu" # replace blah blah

        #boss
        if intro_display == False:
            boss.update(stage_mgr.load_stage())
            if boss.health <= 200 and stage_mgr.load_stage() == 1:
                stage_mgr.save_stage(2) 
                lvlcomplete.play(0.6,1.5,False,0.8)
                battlesong.stop()
                heartpumpySFX.stop()
                return "fighting_dialog"
            elif boss.health <= 100 and stage_mgr.load_stage() == 2 or stage_mgr.load_stage() == 8 or stage_mgr.load_stage() == 7:
                stage_mgr.save_stage(3)
                lvlcomplete.play(0.6,1.5,False,0.8)
                battlesong.stop()
                heartpumpySFX.stop()
                return "fighting_dialog"
            elif boss.health <= 0 and stage_mgr.load_stage() == 3 or stage_mgr.load_stage() == 4 or stage_mgr.load_stage() == 5:
                lvlcomplete.play(0.6,1.5,False,0.8)
                if repressendingpotential == True:
                    print("Boss defeated! | Repress Ending")
                    battlesong.stop()
                    heartpumpySFX.stop()
                    return "main_menu"
                else:
                    print("Boss defeated! | Killer Ending") #
                    battlesong.stop()
                    heartpumpySFX.stop()
                    return "main_menu"
            boss.resolve_collision_with_player(player)
            boss.check_bullet_collisions(vfx_list, damage=5, vfx_list=vfx_list)  # assuming bullets in vfx_list
            if boss.check_player_collision(player):
                player.take_damage(10)
            boss.draw(screen)

        if player.health <= 0:
            fade_surface = pygame.Surface(screen.get_size())
            fade_surface.fill((255, 255, 255))
            for alpha in range(0, 200, 8):  # Fade in
                fade_surface.set_alpha(alpha)
                screen.blit(fade_surface, (0, 0))
                pygame.display.flip()
                pygame.time.delay(5)

            print("Player is dead!")
            heartpumpySFX.stop()
            battlesong.stop()
            return "deadscreen"
        
        # Update & damage
        for splash in wave_splash_list:
            splash.update()
            if splash.check_player_collision(player):
                player.take_damage(5)

        # Draw
        for splash in wave_splash_list:
            splash.draw(screen)
        
        all_raised = all(splash.raised for splash in wave_splash_list)

        if all_raised:
            for splash in wave_splash_list:
                splash.x -= splash.move_speed
                splash.rect = pygame.Rect(int(splash.x), splash.y, splash.width, splash.height)
                if splash.rect.right <= splash.arena_rect.left:
                    splash.done = True

        # Remove finished
        wave_splash_list = [s for s in wave_splash_list if not s.done]
        
        # Update
        for fb in flappybirds:
            fb.update()
            if fb.check_player_collision(player):
                player.take_damage(5)

        # Remove finished
        flappybirds = [fb for fb in flappybirds if not fb.done]

        # Draw
        for fb in flappybirds:
            fb.draw(screen)
        
        # Update spinning balls
        for ball in spinning_balls:
            damage = ball.update()
            if damage:
                player.take_damage(damage)

        spinning_balls = [b for b in spinning_balls if b.alive]

        # Draw spinning balls
        for ball in spinning_balls:
            ball.draw(screen)

        # STAGE 2 ATTACKS
        for lazer in giant_lazers[:]:  # iterate over a copy to safely remove
            lazer.update()
            lazer.draw(screen)
            if lazer.check_player_collision(player):
                player.take_damage(10)
            if lazer.finished:
                giant_lazers.remove(lazer)

        for lazer in giant_lazers:
            lazer.draw(screen)
        for attack in active_rocket_attacks[:]:
            attack.update()
            if attack.finished:
                active_rocket_attacks.remove(attack)
        for attack in active_rocket_attacks:
            attack.draw(screen)

        # To check collisions:
        for attack in active_rocket_attacks:
            if attack.check_player_collision(player) == True:
                print("Player hit by rockets!")
                #should already have the functionality to handle player damage

        if acid_attack is not None:
            acid_attack.update()
            acid_attack.draw(screen)

        for vfx in vfx_list:
            if isinstance(vfx, Bullet):
                if vfx.alive:
                    vfx.update(walls, vfx_list) #BULLETS BULLETS BULLETS BULLETS
            elif isinstance(vfx, Throwable):
                if vfx.spawned_zone:
                    vfx.spawned_zone.check_touch(player.rect, bossArry, boss, player) #PROJECTILES PROJECTILES PROJECTILES PROJECTILES
        
        # SHIELD
        if shield != None:
            if shield.is_active():
                shield.update()
                shield.draw(screen)
                shield.check_block(active_rocket_attacks)
                current_weapon = None
        
        # Draw walls as visible borders
        for wall in walls:
            pygame.draw.rect(screen, (23, 21, 25), wall)
        
        if current_weapon == "sword":    
            sword.update()
            # Check collision with boss:
            if sword.check_hit(boss):
                print("Boss hit by sword!")
                repressendingpotential = False
                if stage_mgr.load_stage == 3 or stage_mgr.load_stage == 4 or stage_mgr.load_stage == 5:
                    if boss.health >= 100:
                        print('no')
                    else:
                        boss.add_health(5)
                elif stage_mgr.load_stage == 2 or stage_mgr.load_stage == 7 or stage_mgr.load_stage == 8:
                    if boss.health >= 200:
                        print('no')
                    else:
                        boss.add_health(5)
                elif stage_mgr.load_stage == 1:
                    if boss.health >= 300:
                        print('no')
                    else:
                        boss.add_health(5)      
            sword.draw(screen)
        if current_weapon == "throwable":
            for vfx in vfx_list:
                if isinstance(vfx, Throwable):
                    vfx.update(walls, bossArry)
                    vfx.draw(screen)
                    if vfx.is_done():
                        vfx_list.remove(vfx)
        for vfx in vfx_list:
            if isinstance(vfx, ParticleEffect): 
                vfx.update()
                vfx.draw(screen)
                if vfx.is_done():
                    vfx_list.remove(vfx)
            elif isinstance(vfx, SpinningBall):
                vfx.update(walls, player, vfx_list)
                vfx.draw(screen)
            else:
                vfx.draw(screen)  # For other VFX types like Throwable, Bullet, etc. (idk why i even put them in the vfx list)
        
        draw_status_texts(screen, font, player, boss, player.ammo, current_weapon, stage_mgr.load_stage(), time_left_minutes, throw_amount)
        
        # charge meter
        if current_weapon == "bullet":
            charge_ratio, _ = player.get_charge_level()
            bar_x = arena_rect.left + 10
            bar_y = arena_rect.top + 10
            block_size = 30
            total_blocks = 4

            for i in range(total_blocks):
                block_x = bar_x + i * block_size
                rect = pygame.Rect(block_x, bar_y, block_size, block_size)
                threshold = (i + 1) / total_blocks
                color = (
                    (190, 255, 234) if i == 0 else
                    (162, 255, 203) if i == 1 else
                    (125, 255, 160) if i == 2 else
                    (93, 255, 115)
                ) if charge_ratio >= threshold else (47, 37, 119)
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, (34, 21, 72), rect, width=1)
        
        # Draw player        
        player.draw(screen)

        pygame.display.flip()
        clock.tick(60) #HOLY GYATT THIS IS A LOT OF CODE :#moneyface:

def ending_kill(screen, state):
    main_image = pygame.image.load("data/artwork/kill_ending.png")

    stage_mgr = StageManager()
    if stage_mgr.load_stage() == None:
        print("Stage not found, setting to default stage 1.")
        stage_mgr.save_stage(1)  # Ensure stage is set to 1 if not found
    print(f"Current stage: {stage_mgr.load_stage()}") #Testing stage loading

    my_font = pygame.font.Font("data/fonts/vcrosdneue.ttf", 30)
    dialogue_manager = DialogueManager(font=my_font, screen=screen)
    isindialouge = False
    pygame.mixer.init()
    word_sound = pygame.mixer.Sound("data/sounds/voice.WAV")

    # Prepare transition intro (fade-in)
    frame_paths = [
        "data/artwork/transitions/frame__0001.png",
        "data/artwork/transitions/frame__0002.png",
        "data/artwork/transitions/frame__0003.png",
        "data/artwork/transitions/frame__0004.png",
        "data/artwork/transitions/frame__0005.png",
        "data/artwork/transitions/frame__0006.png",
        "data/artwork/transitions/frame__0007.png",
        "data/artwork/transitions/frame__0008.png",
        "data/artwork/transitions/frame__0009.png",
        "data/artwork/transitions/frame__0010.png",
        "data/artwork/transitions/frame__0011.png",
        "data/artwork/transitions/frame__0012.png",
        "data/artwork/transitions/frame__0013.png",
        "data/artwork/transitions/frame__0014.png",
        "data/artwork/transitions/frame__0015.png",
        "data/artwork/transitions/frame__0016.png"
    ]

    # Create intro transition (reverse=False)
    intro_transition = TiledTransition(frame_paths, screen.get_size(), reverse=True)
    
    AudioLoop = SFX("data/sounds/tracks/ending_01.mp3")
    AudioLoop.play(1,1,True,0.5)

    # Run intro transition
    clock = pygame.time.Clock()
    while not intro_transition.is_done():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
        screen.blit(main_image, (0, 0))
        intro_transition.update()
        intro_transition.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    screen.blit(main_image, (0, 0))
    pygame.display.flip()

    # Wait time tracking
    leavinshi = [False]

    # Prepare outro transition (fade-out, reverse=True)
    outro_transition = TiledTransition(frame_paths, screen.get_size(), reverse=False)

    running = True
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

        if leavinshi[0]:
            # Run outro transition
            if not outro_transition.is_done():
                screen.blit(main_image, (0, 0))
                outro_transition.update()
                outro_transition.draw(screen)
                pygame.display.flip()
            else:
                # After fade-out, change state
                state.change("credits")
                AudioLoop.stop()
                return "stay"
        else:
            # Still waiting, just show main image
            screen.blit(main_image, (0, 0))
            if isindialouge == False:
                print('f')
                isindialouge = True
                delayed_call(2, lambda: dialogue_manager.queue_dialogue("You stand high above the corpse of the     past.", "???", type_time=2, stay_time=2, char_sound=word_sound, pitch_factor=0.8))
                delayed_call(6, lambda: dialogue_manager.queue_dialogue("You've done it, you've freed yourself,     killed that grand reminder.", "???", type_time=4, stay_time=2, char_sound=word_sound, pitch_factor=0.8))
                delayed_call(12, lambda: dialogue_manager.queue_dialogue("The world is right...", "???", type_time=3, stay_time=2, char_sound=word_sound, pitch_factor=0.8))
                delayed_call(17, lambda: dialogue_manager.queue_dialogue("If only you could change the past...", "???", type_time=5, stay_time=2, char_sound=word_sound, pitch_factor=0.8))
                delayed_call(24, lambda: dialogue_manager.queue_dialogue("Maybe then...", "???", type_time=2, stay_time=2, char_sound=word_sound, pitch_factor=0.8))
                delayed_call(28, lambda: dialogue_manager.queue_dialogue("They wouldn't have passed.", "???", type_time=4, stay_time=2, char_sound=word_sound, pitch_factor=0.8))
                delayed_call(35, lambda: leavinshi.__setitem__(0, True))
        dialogue_manager.update()
        dialogue_manager.draw()
        pygame.display.flip()
        clock.tick(60)

def ending_repress(screen, state):
    main_image = pygame.image.load("data/artwork/repress_ending.png")

    stage_mgr = StageManager()
    if stage_mgr.load_stage() == None:
        print("Stage not found, setting to default stage 1.")
        stage_mgr.save_stage(1)  # Ensure stage is set to 1 if not found
    print(f"Current stage: {stage_mgr.load_stage()}") #Testing stage loading

    my_font = pygame.font.Font("data/fonts/vcrosdneue.ttf", 30)
    dialogue_manager = DialogueManager(font=my_font, screen=screen)
    isindialouge = False
    pygame.mixer.init()
    word_sound = pygame.mixer.Sound("data/sounds/voice.WAV")

    # Prepare transition intro (fade-in)
    frame_paths = [
        "data/artwork/transitions/frame__0001.png",
        "data/artwork/transitions/frame__0002.png",
        "data/artwork/transitions/frame__0003.png",
        "data/artwork/transitions/frame__0004.png",
        "data/artwork/transitions/frame__0005.png",
        "data/artwork/transitions/frame__0006.png",
        "data/artwork/transitions/frame__0007.png",
        "data/artwork/transitions/frame__0008.png",
        "data/artwork/transitions/frame__0009.png",
        "data/artwork/transitions/frame__0010.png",
        "data/artwork/transitions/frame__0011.png",
        "data/artwork/transitions/frame__0012.png",
        "data/artwork/transitions/frame__0013.png",
        "data/artwork/transitions/frame__0014.png",
        "data/artwork/transitions/frame__0015.png",
        "data/artwork/transitions/frame__0016.png"
    ]

    # Create intro transition (reverse=False)
    intro_transition = TiledTransition(frame_paths, screen.get_size(), reverse=True)
    
    AudioLoop = SFX("data/sounds/tracks/ending_01.mp3")
    AudioLoop.play(1,1,True,0.5)

    # Run intro transition
    clock = pygame.time.Clock()
    while not intro_transition.is_done():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
        screen.blit(main_image, (0, 0))
        intro_transition.update()
        intro_transition.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    screen.blit(main_image, (0, 0))
    pygame.display.flip()

    # Wait time tracking
    leavinshi = [False]

    # Prepare outro transition (fade-out, reverse=True)
    outro_transition = TiledTransition(frame_paths, screen.get_size(), reverse=False)

    running = True
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

        if leavinshi[0]:
            # Run outro transition
            if not outro_transition.is_done():
                screen.blit(main_image, (0, 0))
                outro_transition.update()
                outro_transition.draw(screen)
                pygame.display.flip()
            else:
                # After fade-out, change state
                state.change("credits")
                AudioLoop.stop()
                return "stay"
        else:
            # Still waiting, just show main image
            screen.blit(main_image, (0, 0))
            if isindialouge == False:
                print('f')
                isindialouge = True
                delayed_call(2, lambda: dialogue_manager.queue_dialogue("You killed it.", "???", type_time=2, stay_time=2, char_sound=word_sound, pitch_factor=0.8))
                delayed_call(6, lambda: dialogue_manager.queue_dialogue("Your inaction has beaten your enemy...", "???", type_time=2, stay_time=2, char_sound=word_sound, pitch_factor=0.8))
                delayed_call(10, lambda: dialogue_manager.queue_dialogue("Over the years what have you done?", "???", type_time=3, stay_time=2, char_sound=word_sound, pitch_factor=0.8))
                delayed_call(15, lambda: dialogue_manager.queue_dialogue("Ran? Hide? Evaded it all?", "???", type_time=5, stay_time=2, char_sound=word_sound, pitch_factor=0.8))
                delayed_call(22, lambda: dialogue_manager.queue_dialogue("Did avoiding bring any of them back?", "???", type_time=2, stay_time=2, char_sound=word_sound, pitch_factor=0.8))
                delayed_call(26, lambda: dialogue_manager.queue_dialogue("You ponder the future without them...", "???", type_time=4, stay_time=2, char_sound=word_sound, pitch_factor=0.8))
                delayed_call(33, lambda: leavinshi.__setitem__(0, True))
        dialogue_manager.update()
        dialogue_manager.draw()
        pygame.display.flip()
        clock.tick(60)
        
def ending_save(screen, state):
    main_image = pygame.image.load("data/artwork/save_ending.png")

    stage_mgr = StageManager()
    if stage_mgr.load_stage() == None:
        print("Stage not found, setting to default stage 1.")
        stage_mgr.save_stage(1)  # Ensure stage is set to 1 if not found
    print(f"Current stage: {stage_mgr.load_stage()}") #Testing stage loading

    my_font = pygame.font.Font("data/fonts/vcrosdneue.ttf", 30)
    dialogue_manager = DialogueManager(font=my_font, screen=screen)
    isindialouge = False
    pygame.mixer.init()
    word_sound = pygame.mixer.Sound("data/sounds/voice.WAV")

    # Prepare transition intro (fade-in)
    frame_paths = [
        "data/artwork/transitions/frame__0001.png",
        "data/artwork/transitions/frame__0002.png",
        "data/artwork/transitions/frame__0003.png",
        "data/artwork/transitions/frame__0004.png",
        "data/artwork/transitions/frame__0005.png",
        "data/artwork/transitions/frame__0006.png",
        "data/artwork/transitions/frame__0007.png",
        "data/artwork/transitions/frame__0008.png",
        "data/artwork/transitions/frame__0009.png",
        "data/artwork/transitions/frame__0010.png",
        "data/artwork/transitions/frame__0011.png",
        "data/artwork/transitions/frame__0012.png",
        "data/artwork/transitions/frame__0013.png",
        "data/artwork/transitions/frame__0014.png",
        "data/artwork/transitions/frame__0015.png",
        "data/artwork/transitions/frame__0016.png"
    ]

    # Create intro transition (reverse=False)
    intro_transition = TiledTransition(frame_paths, screen.get_size(), reverse=True)
    
    AudioLoop = SFX("data/sounds/tracks/ending_02.mp3")
    AudioLoop.play(1,1,True,0.5)

    # Run intro transition
    clock = pygame.time.Clock()
    while not intro_transition.is_done():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
        screen.blit(main_image, (0, 0))
        intro_transition.update()
        intro_transition.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    screen.blit(main_image, (0, 0))
    pygame.display.flip()

    # Wait time tracking
    leavinshi = [False]

    # Prepare outro transition (fade-out, reverse=True)
    outro_transition = TiledTransition(frame_paths, screen.get_size(), reverse=False)

    running = True
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

        if leavinshi[0]:
            # Run outro transition
            if not outro_transition.is_done():
                screen.blit(main_image, (0, 0))
                outro_transition.update()
                outro_transition.draw(screen)
                pygame.display.flip()
            else:
                # After fade-out, change state
                state.change("credits")
                AudioLoop.stop()
                return "stay"
        else:
            # Still waiting, just show main image
            screen.blit(main_image, (0, 0))
            if isindialouge == False:
                print('f')
                isindialouge = True
                delayed_call(2, lambda: dialogue_manager.queue_dialogue("Acceptance. The final step. I bet it was hard.", "???", type_time=3, stay_time=2, char_sound=word_sound, pitch_factor=0.8))
                delayed_call(7, lambda: dialogue_manager.queue_dialogue("I hope you're able to stay in acceptance.", "???", type_time=4, stay_time=2, char_sound=word_sound, pitch_factor=0.8))
                delayed_call(12, lambda: dialogue_manager.queue_dialogue("But its no personal failure to start over again and you might.", "???", type_time=3, stay_time=2, char_sound=word_sound, pitch_factor=0.8))
                delayed_call(17, lambda: dialogue_manager.queue_dialogue("The old photo, those old gifts, all leading you to somewhere to forget.", "???", type_time=5, stay_time=2, char_sound=word_sound, pitch_factor=0.8))
                delayed_call(24, lambda: dialogue_manager.queue_dialogue("A lot will happen to remind you of those times.", "???", type_time=3, stay_time=2, char_sound=word_sound, pitch_factor=0.8))
                delayed_call(29, lambda: dialogue_manager.queue_dialogue("I'm glad this time however, you didn't kill the boss. Good job.", "???", type_time=4, stay_time=2, char_sound=word_sound, pitch_factor=0.8))
                delayed_call(35, lambda: leavinshi.__setitem__(0, True))
        dialogue_manager.update()
        dialogue_manager.draw()
        pygame.display.flip()
        clock.tick(60)

def creditslogic(screen, state):
    main_image = pygame.image.load("data/artwork/credits_scene.png")

    stage_mgr = StageManager()
    if stage_mgr.load_stage() == None:
        print("Stage not found, setting to default stage 1.")
        stage_mgr.save_stage(1)  # Ensure stage is set to 1 if not found
    stage_mgr.save_stage(1) #just force it since they beat the game already
    print(f"Current stage: {stage_mgr.load_stage()}") #Testing stage loading

    # Prepare transition intro (fade-in)
    frame_paths = [
        "data/artwork/transitions/frame__0001.png",
        "data/artwork/transitions/frame__0002.png",
        "data/artwork/transitions/frame__0003.png",
        "data/artwork/transitions/frame__0004.png",
        "data/artwork/transitions/frame__0005.png",
        "data/artwork/transitions/frame__0006.png",
        "data/artwork/transitions/frame__0007.png",
        "data/artwork/transitions/frame__0008.png",
        "data/artwork/transitions/frame__0009.png",
        "data/artwork/transitions/frame__0010.png",
        "data/artwork/transitions/frame__0011.png",
        "data/artwork/transitions/frame__0012.png",
        "data/artwork/transitions/frame__0013.png",
        "data/artwork/transitions/frame__0014.png",
        "data/artwork/transitions/frame__0015.png",
        "data/artwork/transitions/frame__0016.png"
    ]

    # Create intro transition (reverse=False)
    intro_transition = TiledTransition(frame_paths, screen.get_size(), reverse=True)
    
    AudioLoop = SFX("data/sounds/tracks/credits_loop.mp3")
    AudioLoop.play(1,1,True,0.5)

    # Run intro transition
    clock = pygame.time.Clock()
    while not intro_transition.is_done():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
        screen.blit(main_image, (0, 0))
        intro_transition.update()
        intro_transition.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    screen.blit(main_image, (0, 0))
    pygame.display.flip()

    # Wait time tracking
    leavinshi = False

    # Prepare outro transition (fade-out, reverse=True)
    outro_transition = TiledTransition(frame_paths, screen.get_size(), reverse=False)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    leavinshi = True
        if leavinshi:
            # Run outro transition
            if not outro_transition.is_done():
                screen.blit(main_image, (0, 0))
                outro_transition.update()
                outro_transition.draw(screen)
                pygame.display.flip()
            else:
                # After fade-out, change state
                state.change("main_menu")
                AudioLoop.stop()
                return "stay"
        else:
            # Still waiting, just show main image
            screen.blit(main_image, (0, 0))