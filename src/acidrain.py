import pygame
import random
import time
from util import resource_path

class AcidDrop:
    def __init__(self, x, arena_rect, fall_speed=7, image_path='data/artwork/aciddroplet.png'):
        self.original_width = 12
        self.original_height = 60
        self.width = self.original_width * 1.8
        self.height = self.original_height * 1.8
        self.fall_speed = fall_speed
        self.x = x
        self.y = arena_rect.top
        self.arena_rect = arena_rect
        self.has_landed = False
        self.puddle_spawned = False

        # Load and scale the image
        self.image = resource_path(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def update(self):
        if not self.has_landed:
            self.y += self.fall_speed
            if self.y + self.height >= self.arena_rect.bottom:
                self.y = self.arena_rect.bottom - self.height
                self.has_landed = True
        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class AcidPuddle:
    def __init__(self, x, arena_rect, duration=2.5, damage=5, image_path='data/artwork/acidpuddle.png'):
        self.original_width = 80
        self.original_height = 20
        self.width = self.original_width * 1.3
        self.height = self.original_height * 1.3
        self.duration = duration
        self.damage = damage
        self.active = True
        self.has_damaged = set()
        self.spawn_time = time.time()

        self.x = max(arena_rect.left, min(x, arena_rect.right - self.width))
        self.y = arena_rect.bottom - self.height

        # Load and scale the image
        self.image = resource_path(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def update(self):
        if time.time() - self.spawn_time > self.duration:
            self.active = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def check_collision(self, player):
        if self.active and self.rect.colliderect(player.rect):
            player.take_damage(self.damage)
                
class AcidRainAttack:
    def __init__(self, arena_rect, player, spawn_delay=0.5):
        self.arena_rect = arena_rect
        self.player = player
        self.spawn_delay = spawn_delay
        self.last_spawn_time = 0
        self.spawned = False

        self.acid_drops = []
        self.acid_puddles = []
        self.finished = False

    def update(self):
        now = time.time()

        # Only spawn once
        if not self.spawned and now - self.last_spawn_time > self.spawn_delay:
            for _ in range(3):
                x = random.randint(self.arena_rect.left + 20, self.arena_rect.right - 40)
                drop = AcidDrop(x, self.arena_rect)
                self.acid_drops.append(drop)
            self.last_spawn_time = now
            self.spawned = True

        for drop in self.acid_drops[:]:
            drop.update()
            if drop.has_landed and not drop.puddle_spawned:
                puddle_x = drop.x + drop.width // 2 - 40
                puddle = AcidPuddle(puddle_x, self.arena_rect)
                self.acid_puddles.append(puddle)
                drop.puddle_spawned = True
            if drop.puddle_spawned:
                self.acid_drops.remove(drop)

        for puddle in self.acid_puddles[:]:
            puddle.update()
            puddle.check_collision(self.player)
            if not puddle.active:
                self.acid_puddles.remove(puddle)

        if self.spawned and not self.acid_drops and not self.acid_puddles:
            self.finished = True

    def draw(self, screen):
        for drop in self.acid_drops:
            drop.draw(screen)
        for puddle in self.acid_puddles:
            puddle.draw(screen)

    def is_finished(self):
        return self.finished #heh finished like how im gonna finish you.. wait shit this sounds bad...
