import pygame
from gamelogic import *

class GameState:
    def __init__(self):
        self.current = "main_menu"  # Initial state
        self.pending = False

    def change(self, next_state):
        self.current = next_state
        self.pending = False

state = GameState()

def run_game(screen):
    try:
        logo = pygame.image.load("data/artwork/favicon.png")
        pygame.display.set_icon(logo)
    except Exception as e:
        print("Could not load logo:", e)
    clock = pygame.time.Clock()
    while True:
        if state.current == "main_menu":
            result = mainmenu(screen, state)
        elif state.current == "fighting_dialog":
            result = fightingscreen_dialog_logic(screen, state)
        elif state.current == "battlescreen_01":
            result = battle_screen_01(screen, state)
        elif state.current == "deadscreen":
            result = deadscreen_logic(screen, state)
        elif state.current == "credits":
            result = creditslogic(screen, state)
        elif state.current == "repress":
            result = ending_repress(screen, state)
        elif state.current == "kill":
            result = ending_kill(screen, state)
        elif state.current == "save":
            result = ending_save(screen, state)
        elif state.current == "quit":
            break
        else:
            print("Unknown state:", state.current)
            break

        if result == "quit":
            break
        elif result != "stay":
            state.current = result

        clock.tick(60)

if __name__ == "__main__":
    
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption("OnlyOneBattle")
    run_game(screen)
    pygame.quit()