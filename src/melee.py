import pygame
import time

class Sword:
    def __init__(self, owner, hitbox_size=1.0, damage=1, cooldown=0.8):
        self.owner = owner
        self.damage = damage
        self.cooldown = cooldown  # seconds between attacks
        self.hitbox_size = hitbox_size

        # Sword visual rectangle parameters (just for showing the sword)
        self.color = (0, 0, 255)
        self.width = 10
        self.height = owner.rect.height + 10

        # Timer for active attack duration
        self.timer = 0
        self.active = False

        self.last_attack_time = 0

        # Hitbox will be a circle around the sword's position
        self.hitbox_center = (0, 0)
        self.hitbox_radius = (self.width + self.height) / 4 * hitbox_size  # approx radius

        # Visual hitbox rect (for debugging/drawing)
        self.hitbox_rect = pygame.Rect(0, 0, self.width, self.height)

    def attack(self):
        now = time.time()
        if not self.active and (now - self.last_attack_time) >= self.cooldown:
            self.active = True
            self.timer = int(self.cooldown * 60)  # Convert cooldown to frames (assuming 60 FPS)
            self.last_attack_time = now

            # Set hitbox position based on owner facing
            if self.owner.facing_right:
                x = self.owner.rect.right + self.hitbox_radius
            else:
                x = self.owner.rect.left - self.hitbox_radius

            y = self.owner.rect.centery
            self.hitbox_center = (x, y)

            # Update visual rect for drawing
            self.hitbox_rect.center = self.hitbox_center

    def update(self):
        # Decrease active timer
        if self.timer > 0:
            self.timer -= 1
            if self.timer == 0:
                self.active = False

        # Update hitbox position relative to owner while active
        if self.active:
            if self.owner.facing_right:
                x = self.owner.rect.right + self.hitbox_radius
            else:
                x = self.owner.rect.left - self.hitbox_radius
            y = self.owner.rect.centery
            self.hitbox_center = (x, y)
            self.hitbox_rect.center = self.hitbox_center

    def draw(self, surface):
        # Draw sword rectangle near player
        if self.owner.facing_right:
            sword_rect = pygame.Rect(
                self.owner.rect.right, 
                self.owner.rect.y + (self.owner.rect.height - self.height) // 2, 
                self.width, 
                self.height
            )
        else:
            sword_rect = pygame.Rect(
                self.owner.rect.left - self.width, 
                self.owner.rect.y + (self.owner.rect.height - self.height) // 2, 
                self.width, 
                self.height
            )
        pygame.draw.rect(surface, self.color, sword_rect)

        # Draw hitbox circle if active (for debugging)
        if self.active:
            pygame.draw.circle(surface, (255, 0, 0), (int(self.hitbox_center[0]), int(self.hitbox_center[1])), int(self.hitbox_radius), 2)

    def check_hit(self, boss):
        if not self.active:
            return False

        # Check collision between sword's circular hitbox and boss rect
        # Approximate circle-rectangle collision:
        circle_x, circle_y = self.hitbox_center #circwle uwu :3
        rect = boss.rect

        closest_x = max(rect.left, min(circle_x, rect.right))
        closest_y = max(rect.top, min(circle_y, rect.bottom))

        dist_x = circle_x - closest_x
        dist_y = circle_y - closest_y

        distance_sq = dist_x ** 2 + dist_y ** 2
        if distance_sq <= self.hitbox_radius ** 2:
            return True

        return False
