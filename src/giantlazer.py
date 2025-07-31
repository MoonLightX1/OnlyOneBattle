import pygame

from util import *

class GiantLazer:
    def __init__(self, boss, arena_rect, width=24, rise_speed=12, sweep_speed=7):
        self.arena_rect = arena_rect
        self.rise_speed = rise_speed
        self.sweep_speed = sweep_speed

        # Start from the ground
        self.x = boss.rect.centerx - width // 2 + 80
        self.top_y = arena_rect.bottom
        self.target_top_y = arena_rect.top
        self.height = 0

        self.state = "rising"
        self.finished = False

        self.hasplayedaudi = False
        self.lazersfx = SFX("data/sounds/lazer sfx.mp3")

        # Load the image
        self.base_image = resource_path("data/artwork/lazer.png").convert_alpha()
        self.width = width
        self.color = (255, 0, 0)  # Optional, in case of fallback

    def update(self):
        if self.state == "rising":
            if self.hasplayedaudi == False:
                self.lazersfx.play(0.6,1.5,False,1)
                self.hasplayedaudi = True
            self.top_y -= self.rise_speed
            if self.top_y <= self.target_top_y:
                self.top_y = self.target_top_y
                self.height = self.arena_rect.bottom
                self.state = "sweeping"

        elif self.state == "sweeping":
            self.x -= self.sweep_speed
            if self.x <= self.arena_rect.left + 60:
                self.x = self.arena_rect.left + 60
                self.state = "done"
                if self.hasplayedaudi == True: 
                    self.lazersfx.stop()

        elif self.state == "done":
            self.finished = True

    def stop_currentsfx(self):
        self.lazersfx.stop()

    def draw(self, screen):
        if self.state == "rising":
            dynamic_height = self.arena_rect.bottom - self.top_y
        else:
            dynamic_height = self.height

        lazer_image = pygame.transform.scale(self.base_image, (self.width, dynamic_height))
        screen.blit(lazer_image, (self.x, self.top_y))


    def check_player_collision(self, player):
        if self.state in ["sweeping", "done"]:
            rect = pygame.Rect(self.x, self.top_y, self.width, self.height)
            return rect.colliderect(player.rect)
        return False
