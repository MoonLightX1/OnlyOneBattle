import time
import pygame
import math

class Throwable:
    def __init__(self, x, y, target_x, target_y, power=15):
        self.x = x
        self.y = y
        self.gravity = 0.4
        self.radius = 20
        self.color = (255, 255, 255)  # White square
        self.alive = True
        self.vx, self.vy = self.calculate_velocity(x, y, target_x, target_y, power)
        self.rect = pygame.Rect(x, y, self.radius, self.radius)
        self.spawned_zone = None  # The red zone that appears on impact
        self.iscooldowndone = False

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

        # Apply gravity
        self.vy += self.gravity

        # Determine orientation based on collision
        # STOP WITH ALL OF THIS MATH SHIT

        # Move
        self.x += self.vx
        self.y += self.vy
        self.rect.topleft = (int(self.x), int(self.y))

        for wall in walls:
            if self.rect.colliderect(wall):
                if self.alive and not self.spawned_zone:
                    self.alive = False

                    # Calculate collision side
                    dx = self.rect.centerx - wall.centerx
                    dy = self.rect.centery - wall.centery

                    if abs(dx) > abs(dy):
                        orientation = "left" if dx < 0 else "right"
                    else:
                        orientation = "up" if dy < 0 else "down"

                    self.spawned_zone = DamageZone(self.rect.centerx, self.rect.centery, orientation)

                break
        for b in boss:
            if self.rect.colliderect(b):
                if self.alive and not self.spawned_zone:
                    self.alive = False

                    dx = self.rect.centerx - b.rect.centerx
                    dy = self.rect.centery - b.rect.centery

                    if abs(dx) > abs(dy):
                        orientation = "left" if dx < 0 else "right"
                    else:
                        orientation = "up" if dy < 0 else "down"

                    offset_x = self.rect.centerx - b.rect.centerx
                    offset_y = self.rect.centery - b.rect.centery

                    # Attach to boss with rotation
                    self.spawned_zone = DamageZone(b.rect.centerx, b.rect.centery, orientation, anchor=b, offset=(offset_x, offset_y))
                break

    def draw(self, screen):
        if self.alive:
            pygame.draw.rect(screen, self.color, self.rect)
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
        self.color = (255, 100, 100)
        self.anchor = anchor
        self.offset = offset

        self.width, self.height = (12, 40) if orientation in ("down", "up") else (40, 12)
        self.rect = pygame.Rect(x, y, self.width, self.height)

        self.rotation_angle = 0
        self.damage_cooldown = 0.5  # seconds

        self.last_damage_time_boss = 0
        self.last_damage_time_player = 0

    def update_position(self):
        if self.anchor:
            self.rotation_angle = getattr(self.anchor, "rotation_angle", 0)
            ox, oy = self.offset
            angle_rad = math.radians(-self.rotation_angle)
            rotated_x = ox * math.cos(angle_rad) - oy * math.sin(angle_rad)
            rotated_y = ox * math.sin(angle_rad) + oy * math.cos(angle_rad)

            anchor_cx = self.anchor.rect.centerx
            anchor_cy = self.anchor.rect.centery

            self.rect.topleft = (anchor_cx + rotated_x - self.width // 2,
                                 anchor_cy + rotated_y - self.height // 2)

    def draw(self, screen):
        self.update_position()
        rotated_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        rotated_surf.fill(self.color)
        rotated_surf = pygame.transform.rotate(rotated_surf, self.rotation_angle)
        new_rect = rotated_surf.get_rect(center=self.rect.center)
        screen.blit(rotated_surf, new_rect.topleft)

    def check_touch(self, player_rect, bossArry, boss, player):
        self.update_position()
        now = time.time()

        # Damage player if they're inside and cooldown passed
        if self.rect.colliderect(player_rect) and now - self.last_damage_time_player >= self.damage_cooldown:
            player.take_damage(3)
            self.last_damage_time_player = now

        # Damage boss if it's still in the zone
        for b in bossArry:
            if self.rect.colliderect(b.rect) and now - self.last_damage_time_boss >= self.damage_cooldown:
                boss.take_damage(1)
                self.last_damage_time_boss = now

    def is_expired(self):
        return time.time() - self.creation_time > 5