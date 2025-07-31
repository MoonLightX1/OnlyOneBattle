import pygame
import time
from decimal import Decimal

from bullets import *
from projectiles import *
from util import SFX, resource_path

class Boss:
    def __init__(self, image_path, x, y, width, height, arena_rect, stagelvl=1):
        self.image_path = image_path
        self.starting_x = x
        self.starting_y = y
        self.x = x
        self.y = y
        self.width = width
        self.stagelvl = stagelvl
        self.height = height
        self.dx = 0
        self.dy = 0
        self.health = 100
        self.last_damage_time = 0
        self.damage_cooldown = 0.1 
        self.last_damage_time_sep = 0
        self.damage_cooldown_sep = 0.1 
        self.last_heal_time = 0
        self.heal_cooldown = 0.1
        
        self.arena_rect = arena_rect
        self.speed_x = 2
        self.speed_y = 1.5
        self.direction_x = 1  # 1 = right, -1 = left
        self.direction_y = 1  # 1 = down, -1 = up
        
        self.rotation_angle = 0
        self.rotation_speed = 1.5

        self.image_original = resource_path(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image_original, (self.width, self.height))

        # Transition
        self.transition_brightness = 255
        self.transition_speed = 5

        # Rect for collision
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        self.damageSFX = SFX("data/sounds/damage sfx.mp3")
        self.deathSFX = SFX("data/sounds/death sfx.mp3")

        self.hastakenbigdmg = False

    def update(self, stagelvl):
        # Move horizontally
        self.x += self.speed_x * self.direction_x
        if self.x <= self.arena_rect.left or self.x + self.width >= self.arena_rect.right:
            self.direction_x *= -1

        # Move vertically
        self.y += self.speed_y * self.direction_y
        if self.y <= self.arena_rect.top or self.y + self.height >= self.arena_rect.bottom:
            self.direction_y *= -1

        # Fade in transition
        if self.transition_brightness > 0:
            self.transition_brightness = max(0, self.transition_brightness - self.transition_speed)

        # Update rect
        self.rect.topleft = (self.x, self.y)
        
        self.rotation_angle = (self.rotation_angle + self.rotation_speed) % 360
        if stagelvl == 3 or stagelvl == 4 or stagelvl == 5:
            self.take_damage_sepcooldown(0.1)

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.image, -self.rotation_angle)
        rotated_rect = rotated_image.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))

        if self.transition_brightness > 0:
            bright_surface = rotated_image.copy()
            overlay = pygame.Surface(bright_surface.get_size(), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, self.transition_brightness))
            bright_surface.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
            screen.blit(bright_surface, rotated_rect.topleft)
        else:
            screen.blit(rotated_image, rotated_rect.topleft)

    def take_damage(self, amount):
        self.damageSFX.play(0.4, 1, False, 0.3)
        if amount > 0.11:
            self.hastakenbigdmg = True
        now = time.time()
        if now - self.last_damage_time >= self.damage_cooldown:
            self.health = round(self.health - amount, 1)
            self.last_damage_time = now
            print(f"Boss took {amount} damage! Health now: {self.health}")
            if self.health <= 0:
                self.deathSFX.play(0.4, 1, False, 0.4)
                self.health = 0
                print('dead')
                
    def take_damage_sepcooldown(self, amount):
        self.damageSFX.play(0.4, 1, False, 0.3)
        if amount > 0.11:
            self.hastakenbigdmg = True
        now = time.time()
        if now - self.last_damage_time_sep >= self.damage_cooldown_sep:
            self.health = round(self.health - amount, 1)
            self.last_damage_time_sep = now
            print(f"Boss took {amount} damage! Health now: {self.health}")
            if self.health <= 0:
                self.deathSFX.play(0.4, 1, False, 0.4)
                self.health = 0
                print('dead')
                    
    def check_bullet_collisions(self, projectiles, damage=10, vfx_list=None):
        for obj in projectiles:
        # Check if it's a Bullet and has required attributes
            if isinstance(obj, Bullet) and getattr(obj, 'alive', False) and hasattr(obj, 'rect'):
                if self.rect.colliderect(obj.rect):
                    self.take_damage(damage)
                    obj.alive = False
                    vfx_list.append(ParticleEffect(self.rect.centerx, self.rect.centery))
            if isinstance(obj, Throwable) and getattr(obj, 'alive', False) and hasattr(obj, 'rect'):
                if self.rect.colliderect(obj.rect):
                    self.take_damage(0.13) 

    def add_health(self, amount):
        now = time.time()
        print("Time since last heal:", now - self.last_heal_time)
        if now - self.last_heal_time >= self.heal_cooldown:
            self.health = round(self.health + amount, 1)
            self.last_heal_time = now
            print(f"Boss got {amount} hearts! Health now: {self.health}")

    def check_player_collision(self, player):
        return self.rect.colliderect(player.rect)

    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.rect.topleft = (x, y)
    
    def resolve_collision_with_player(self, player):
        if self.rect.colliderect(player.rect):
            # Push player out of the boss's body
            # WAIT I DIDNT EVEN REALIZE I ADDED THIS IM SO SMART WHAT

            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery

            # Decide dominant axis
            if abs(dx) > abs(dy):  # Horizontal push
            # what the fuck i can math the math
                if dx > 0:
                    player.rect.x = self.rect.right
                else:
                    player.rect.x = self.rect.left - player.rect.width
            else:  # Vertical push
                if dy > 0:
                    player.rect.y = self.rect.bottom
                else:
                    player.rect.y = self.rect.top - player.rect.height

            # Update player rect
            player.rect.topleft = (player.rect.x, player.rect.y)
        