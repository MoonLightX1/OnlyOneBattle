import math
import pygame
from vfx import ParticleEffect

class Bullet:
    def __init__(self, x, y, target_x, target_y, power=25):
        self.x = x
        self.y = y
        self.power = power
        self.gravity = 0.5
        self.radius = 5  # for future circular hit or trail fx

        # Calculate initial velocity toward mouse target
        dx = target_x - x
        dy = target_y - y
        dist = math.hypot(dx, dy)
        if dist == 0:
            dist = 1  # prevent division by zero
        self.vx = (dx / dist) * self.power
        self.vy = (dy / dist) * self.power

        # Create a red rectangle surface
        self.rect = pygame.Rect(x, y, 30, 6)
        self.image = pygame.Surface((30, 6), pygame.SRCALPHA)
        self.image.fill((255, 0, 0))  # red bullet

        self.alive = True  # Can be used for cleanup or collision

    # DO WE EVEN USE THIS SHIT??? WTF
    # def calculate_velocity(self, x, y, target_x, target_y, speed):
    #     # Calculate the vector from bullet to target
    #     dx = target_x - x 
    #     dy = target_y - y 
    #     dist = math.hypot(dx, dy)
    #     if dist == 0:
    #         return 0, 0
    #     # Normalize vector and multiply by speed for initial velocity
    #     vx = (dx / dist) * (speed/5)
    #     vy = (dy / dist) * (speed/5)
    #     return vx, vy

    def update(self, walls, vfx_list):
            # Apply gravity
        self.vy += self.gravity

        # Update position
        self.x += self.vx
        self.y += self.vy 
        self.rect.topleft = (self.x, self.y) # EW I DID MORE MATH :throwsup:

        for wall in walls:
            if self.rect.colliderect(wall):
                self.alive = False
                vfx_list.append(ParticleEffect(self.rect.centerx, self.rect.centery))
                break


    def draw(self, screen):
        # Calculate angle from current velocity
        angle = math.degrees(math.atan2(-self.vy, self.vx))

        # Rotate the image to match direction
        rotated = pygame.transform.rotate(self.image, angle)
        rotated_rect = rotated.get_rect(center=self.rect.center)

        # Draw rotated bullet
        screen.blit(rotated, rotated_rect)
