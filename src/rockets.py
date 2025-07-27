import pygame
import math
import time
from vfx import ParticleEffect 

class Rocket:
    def __init__(self, center_pos, angle, radius, player, speed=3, color=(255, 100, 100), size=12):
        self.player = player
        self.speed = speed
        self.color = color
        self.size = size
        
        self.center_x, self.center_y = center_pos
        self.angle = angle
        self.radius = 10  # fixed radius for rocket orbit
        self.x = self.center_x + math.cos(angle) * radius
        self.y = self.center_y + math.sin(angle) * radius

        self.spawn_time = time.time()
        self.exploded = False
        self.rect = pygame.Rect(self.x - radius, self.y - radius, radius * 2, radius * 2)

        self.vx = 0
        self.vy = 0

    def update(self):
        if self.exploded:
            return

        dx = self.player.rect.centerx - self.x
        dy = self.player.rect.centery - self.y
        dist = math.hypot(dx, dy)
        if dist == 0:
            dist = 1
        
        homing_strength = 0.05
        dir_x = dx / dist
        dir_y = dy / dist

        self.vx = (1 - homing_strength) * self.vx + homing_strength * dir_x * self.speed
        self.vy = (1 - homing_strength) * self.vy + homing_strength * dir_y * self.speed

        self.x += self.vx
        self.y += self.vy

        self.rect = pygame.Rect(self.x - self.radius - 5, self.y - self.radius - 5, (self.radius + 5) * 2, (self.radius + 5) * 2)


        # Explode if 3 seconds passed OR collide with player
        if time.time() - self.spawn_time >= 4.95:
            self.explode()

    def explode(self):
        if not self.exploded:
            self.exploded = True
            print("Rocket exploded!")

    def draw(self, screen):
        if self.exploded:
            return
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

class RocketsAttack:
    def __init__(self, boss, player, arena_rect, num_rockets=8, radius=80):
        self.rockets = []
        self.player = player
        self.arena_rect = arena_rect

        center = boss.rect.center
        for i in range(num_rockets):
            angle = (2 * math.pi / num_rockets) * i
            rocket = Rocket(center, angle, radius, player)
            self.rockets.append(rocket)
        
        self.explosions = []
        self.finished = False

    def update(self):
        if self.finished:
            return

        all_exploded = True
        for rocket in self.rockets[:]:  # iterate over a copy because we may remove
            rocket.update()
            if rocket.exploded:
                # Trigger explosion VFX, then remove rocket from list
                self.explosions.append(ParticleEffect(rocket.x, rocket.y, size_multiplier=2))  # bigger explosion
                self.rockets.remove(rocket)
            else:
                all_exploded = False

        for explosion in self.explosions[:]:
            explosion.update()
            if explosion.is_done():
                self.explosions.remove(explosion)

        if all_exploded and not self.explosions:
            self.finished = True

    def draw(self, screen):
        for rocket in self.rockets:
            rocket.draw(screen)
        for explosion in self.explosions:
            explosion.draw(screen)

    def check_player_collision(self, player):
        for rocket in self.rockets:
            if not rocket.exploded:
                if rocket.rect.colliderect(player.rect):
                    print("Collision detected!")
                    rocket.explode()
                    player.take_damage(5)
                    self.explosions.append(ParticleEffect(rocket.x, rocket.y))
                    return True
        return False