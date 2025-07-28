import random
import pygame

class GlitchyArena:
    def __init__(self, image_path, pos):
        self.image = pygame.image.load(image_path).convert()
        self.original = self.image.copy()
        self.rect = self.image.get_rect(topleft=pos)
        self.glitch_timer = 0
        self.glitch_active = False

    def trigger_glitch(self):
        if random.random() < 0.01:  # 1% chance per frame
            self.glitch_timer = random.randint(5, 15)
            self.glitch_active = True

    def apply_glitch(self):
        if self.glitch_active and self.glitch_timer > 0:
            glitch_surface = self.original.copy()

            # Apply line shifts
            for _ in range(5):
                y = random.randint(0, self.rect.height - 5)
                height = random.randint(2, 6)
                offset = random.randint(-20, 20)

                # NEW: clamp height to fit within surface
                max_height = self.rect.height - y
                safe_height = min(height, max_height)

                slice = glitch_surface.subsurface(pygame.Rect(0, y, self.rect.width, safe_height))
                self.image.blit(slice, (offset, y))


            # Optional: add scanline
            if random.random() < 0.3:
                for y in range(0, self.rect.height, 4):
                    pygame.draw.line(self.image, (30, 30, 30), (0, y), (self.rect.width, y))

            self.glitch_timer -= 1
        else:
            self.image = self.original.copy()
            self.glitch_active = False

    def update(self):
        self.trigger_glitch()
        self.apply_glitch()

    def draw(self, surface):
        surface.blit(self.image, self.rect)
