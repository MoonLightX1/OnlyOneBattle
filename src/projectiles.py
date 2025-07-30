import time
import pygame
import math

from util import resource_path

class Throwable:
    def __init__(self, x, y, target_x, target_y, power=15):
        self.x = x
        self.y = y
        self.gravity = 0.4
        self.radius = 20
        self.alive = True
        self.vx, self.vy = self.calculate_velocity(x, y, target_x, target_y, power)
        self.rect = pygame.Rect(x, y, self.radius, self.radius)
        self.spawned_zone = None
        self.iscooldowndone = False
        self.image = resource_path("data/artwork/throwables.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.radius*2, self.radius*2))  #resized only slightly
    def calculate_velocity(self, x, y, target_x, target_y, power):
        dx = target_x - x
        dy = target_y - y
        dist = math.hypot(dx, dy)
        if dist == 0:
            return 0, 0
        return (dx / dist) * power, (dy / dist) * power

    def update(self, walls, boss):
        if not self.alive:
            return

        self.vy += self.gravity
        self.x += self.vx
        self.y += self.vy
        self.rect.topleft = (int(self.x), int(self.y))

        for wall in walls:
            if self.rect.colliderect(wall):
                if self.alive and not self.spawned_zone:
                    self.alive = False
                    dx = self.rect.centerx - wall.centerx
                    dy = self.rect.centery - wall.centery
                    orientation = "left" if abs(dx) > abs(dy) and dx < 0 else \
                                  "right" if abs(dx) > abs(dy) else \
                                  "up" if dy < 0 else "down"
                    self.spawned_zone = DamageZone(self.rect.centerx, self.rect.centery, orientation)
                break

        for b in boss:
            if self.rect.colliderect(b):
                if self.alive and not self.spawned_zone:
                    self.alive = False
                    dx = self.rect.centerx - b.rect.centerx
                    dy = self.rect.centery - b.rect.centery
                    orientation = "left" if abs(dx) > abs(dy) and dx < 0 else \
                                  "right" if abs(dx) > abs(dy) else \
                                  "up" if dy < 0 else "down"
                    offset_x = self.rect.centerx - b.rect.centerx
                    offset_y = self.rect.centery - b.rect.centery
                    self.spawned_zone = DamageZone(b.rect.centerx, b.rect.centery, orientation, anchor=b, offset=(offset_x, offset_y))
                break

    def draw(self, screen):
        if self.alive:
            screen.blit(self.image, self.rect.topleft)
        if self.spawned_zone:
            self.spawned_zone.draw(screen)

    def is_done(self):
        if self.spawned_zone and self.spawned_zone.is_expired():
            self.spawned_zone = None
        return not self.alive and self.spawned_zone is None

class DamageZone:
    def __init__(self, x, y, orientation="down", anchor=None, offset=(0, 0)):
        self.orientation = orientation
        self.creation_time = time.time()
        self.anchor = anchor
        self.offset = offset
        self.image_vertical = resource_path("data/artwork/goopuddle_side.png").convert_alpha()
        self.image_horizontal = resource_path("data/artwork/goop_normal.png").convert_alpha()
        self.image = (self.image_vertical if orientation in ("down", "up")
                      else self.image_horizontal)
        self.image = pygame.transform.scale_by(self.image, 1.5)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = pygame.Rect(x, y, self.width, self.height)

        self.rotation_angle = 0
        self.damage_cooldown = 0.5  # seconds

        self.last_damage_time_boss = 0
        self.last_damage_time_player = 0

    def update_position(self):
        if self.anchor:
            self.rotation_angle = getattr(self.anchor, "rotation_angle", 0)
            # Convert the offset to a rotated vector
            ox, oy = self.offset
            angle_rad = math.radians(-self.rotation_angle)

            rotated_offset_x = ox * math.cos(angle_rad) - oy * math.sin(angle_rad)
            rotated_offset_y = ox * math.sin(angle_rad) + oy * math.cos(angle_rad)

            # Get the anchor's center position
            anchor_center_x = self.anchor.rect.centerx
            anchor_center_y = self.anchor.rect.centery

            # Final position is anchor's center + rotated offset
            zone_center_x = anchor_center_x + rotated_offset_x
            zone_center_y = anchor_center_y + rotated_offset_y

            # Set the center of the rect precisely
            self.rect.center = (round(zone_center_x), round(zone_center_y))

    def draw(self, screen):
        self.update_position()
        rotated_img = pygame.transform.rotate(self.image, self.rotation_angle)
        new_rect = rotated_img.get_rect(center=self.rect.center)
        screen.blit(rotated_img, new_rect.topleft)

    def check_touch(self, player_rect, bossArry, boss, player):
        self.update_position()
        now = time.time()
        if self.rect.colliderect(player_rect) and now - self.last_damage_time_player >= self.damage_cooldown:
            player.take_damage(3)
            self.last_damage_time_player = now
        for b in bossArry:
            if self.rect.colliderect(b.rect) and now - self.last_damage_time_boss >= self.damage_cooldown:
                boss.take_damage(1)
                self.last_damage_time_boss = now

    def is_expired(self):
        return time.time() - self.creation_time > 5
