import pygame
import random
from vfx import ParticleEffect

class SpinningBall:
    def __init__(self, x, y, dx, dy, arena_rect):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.radius = 6
        self.angle = 0
        self.rotation_speed = 10  # degrees per frame
        self.image_original = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image_original, (255, 255, 0), (self.radius, self.radius), self.radius)
        self.arena_rect = arena_rect
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
        self.alive = True

    def update(self, walls, player, vfx_list):
        if not self.alive:
            return

        self.x += self.dx
        self.y += self.dy
        self.rect.topleft = (self.x - self.radius, self.y - self.radius)

        # Check collision with player
        if self.rect.colliderect(player.rect):
            player.take_damage(5)
            vfx_list.append(ParticleEffect(self.x, self.y))
            self.alive = False
            return

        # Check collision with walls
        for wall in walls:
            if self.rect.colliderect(wall):
                vfx_list.append(ParticleEffect(self.x, self.y))
                self.alive = False
                return
        self.angle = (self.angle + self.rotation_speed) % 360

    def draw(self, screen):
        if self.alive:
            rotated_image = pygame.transform.rotate(self.image_original, self.angle)
            rect = rotated_image.get_rect(center=(int(self.x), int(self.y)))
            screen.blit(rotated_image, rect.topleft)

