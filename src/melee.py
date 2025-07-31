import pygame
import time

from util import SFX, resource_path

class Sword:
    def __init__(self, owner, hitbox_size=1.0, damage=1, cooldown=0.8, image_path="data/artwork/dagger.png"):
        self.owner = owner
        self.damage = damage
        self.cooldown = cooldown  # seconds between attacks
        self.hitbox_size = hitbox_size

        # Load sword image
        self.image = resource_path(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (20, 40))
        self.original_image = self.image
        self.width, self.height = self.image.get_size()

        # Timer for attack duration
        self.timer = 0
        self.active = False
        self.last_attack_time = 0

        # Hitbox
        self.hitbox_center = (0, 0)
        self.hitbox_radius = (self.width + self.height) / 4 * hitbox_size
        self.hitbox_rect = pygame.Rect(0, 0, self.width, self.height)
        
        self.daggerhitSFX = SFX("data/sounds/dagger sfx.mp3")

    def attack(self):
        now = time.time()
        if not self.active and (now - self.last_attack_time) >= self.cooldown:
            self.daggerhitSFX.play(0.6,1.5,False,0.7)
            self.active = True
            self.timer = int(self.cooldown * 60)
            self.last_attack_time = now

            # Update hitbox position based on facing
            self._update_hitbox_pos()

    def update(self):
        if self.timer > 0:
            self.timer -= 1
            if self.timer == 0:
                self.active = False
        if self.active:
            self._update_hitbox_pos()

    def _update_hitbox_pos(self):
        if self.owner.facing_right:
            x = self.owner.rect.right + self.hitbox_radius
        else:
            x = self.owner.rect.left - self.hitbox_radius
        y = self.owner.rect.centery
        self.hitbox_center = (x, y)
        self.hitbox_rect.center = self.hitbox_center

    def draw(self, surface):
        # Position the sword image
        if self.owner.facing_right:
            sword_pos = (
                self.owner.rect.right,
                self.owner.rect.y + (self.owner.rect.height - self.height) // 2
            )
            sword_img = self.original_image
        else:
            sword_pos = (
                self.owner.rect.left - self.width,
                self.owner.rect.y + (self.owner.rect.height - self.height) // 2
            )
            sword_img = pygame.transform.flip(self.original_image, True, False)

        surface.blit(sword_img, sword_pos)

    def check_hit(self, boss):
        if not self.active:
            return False

        circle_x, circle_y = self.hitbox_center
        rect = boss.rect

        closest_x = max(rect.left, min(circle_x, rect.right))
        closest_y = max(rect.top, min(circle_y, rect.bottom))

        dist_x = circle_x - closest_x
        dist_y = circle_y - closest_y

        return (dist_x ** 2 + dist_y ** 2) <= self.hitbox_radius ** 2
