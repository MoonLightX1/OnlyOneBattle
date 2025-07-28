import pygame
import math
import time

class Shield:
    def __init__(self, player, duration=20, cooldown=10, image_path="data/artwork/shield.png"):
        self.player = player
        self.length = 80
        self.width = 20
        self.angle = 0

        # Load and scale shield image
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (self.length, self.width))
        self.image = self.original_image

        # Collision rect
        self.rect = self.original_image.get_rect()
        self.center_x = 0
        self.center_y = 0

        # Activation and cooldown control
        self.active = False
        self.ready = True
        self.duration = duration
        self.cooldown_time = cooldown
        self.activation_time = 0
        self.cooldown_start = 0

    def activate(self):
        if self.ready:
            self.active = True
            self.ready = False
            self.activation_time = time.time()
            print("Shield activated")

    def update(self):
        if self.active and (time.time() - self.activation_time >= self.duration):
            self.active = False
            self.cooldown_start = time.time()
            print("Shield deactivated - entering cooldown")

        if not self.active and not self.ready and (time.time() - self.cooldown_start >= self.cooldown_time):
            self.ready = True
            print("Shield ready again")

        if self.active:
            self.update_position()

    def update_position(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dx = mouse_x - self.player.rect.centerx
        dy = mouse_y - self.player.rect.centery
        self.angle = math.atan2(dy, dx)

        offset_distance = 40
        self.center_x = self.player.rect.centerx + math.cos(self.angle) * offset_distance
        self.center_y = self.player.rect.centery + math.sin(self.angle) * offset_distance

        self.rect = pygame.Rect(0, 0, self.length, self.width)
        self.rect.center = (self.center_x, self.center_y)

    def draw(self, screen):
        if not self.active:
            return

        # Rotate and draw the image
        rotated_image = pygame.transform.rotate(self.original_image, -math.degrees(self.angle))
        rotated_rect = rotated_image.get_rect(center=(self.center_x, self.center_y))
        screen.blit(rotated_image, rotated_rect)

    def check_block(self, rocket_attacks):
        if not self.active:
            return
        for attack in rocket_attacks:
            for rocket in attack.rockets:
                if self.rect.colliderect(rocket.rect):
                    print("Rocket blocked by shield!")
                    rocket.explode()

    def is_active(self):
        return self.active

    def is_ready(self):
        return self.ready
