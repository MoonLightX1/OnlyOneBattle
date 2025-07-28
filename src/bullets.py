import math
import pygame
from vfx import ParticleEffect

class Bullet:
    def __init__(self, x, y, target_x, target_y, image_path, power=25):
        self.x = x
        self.y = y
        self.power = power
        self.gravity = 0.5
        self.radius = 5  # for future circular hit or trail fx

        # Load bullet image
        self.image = pygame.image.load(image_path).convert_alpha()
        self.original_image = self.image  # keep original for rotation
        self.rect = self.image.get_rect(center=(x, y))

        # Calculate initial velocity toward mouse target
        dx = target_x - x
        dy = target_y - y
        dist = math.hypot(dx, dy)
        if dist == 0:
            dist = 1  # prevent division by zero
        self.vx = (dx / dist) * self.power
        self.vy = (dy / dist) * self.power

        self.alive = True  # Can be used for cleanup or collision

    def update(self, walls, vfx_list):
        # Apply gravity
        self.vy += self.gravity

        # Update position
        self.x += self.vx
        self.y += self.vy 
        self.rect.center = (self.x, self.y)

        for wall in walls:
            if self.rect.colliderect(wall):
                self.alive = False
                vfx_list.append(ParticleEffect(self.rect.centerx, self.rect.centery))
                break

    def draw(self, screen):
        # Calculate angle from current velocity
        angle = math.degrees(math.atan2(-self.vy, self.vx))

        # Rotate the image to match direction
        rotated = pygame.transform.rotate(self.original_image, angle)
        rotated_rect = rotated.get_rect(center=self.rect.center)

        # Draw rotated bullet
        screen.blit(rotated, rotated_rect)
