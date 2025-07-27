import pygame

class WaveSplashRect:
    def __init__(self, x, arena_rect, height_rank, width=12, rise_speed=5, move_speed=4):
        self.start_x = x            # Store the starting x, don’t overwrite this
        self.x = x                  # Current moving x position
        self.width = width
        self.full_height = [40, 80, 120, 160, 160, 120, 80, 40][height_rank]
        self.height = 0
        self.arena_rect = arena_rect
        self.rise_speed = rise_speed
        self.move_speed = move_speed
        self.raised = False
        self.done = False
        self.y = self.arena_rect.bottom - self.height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        if not self.raised:
            self.height += self.rise_speed
            if self.height >= self.full_height:
                self.height = self.full_height
                self.raised = True

        # Keep bottom aligned to arena bottom
        self.y = self.arena_rect.bottom - self.height
        self.rect = pygame.Rect(int(self.x), self.y, self.width, self.height)


    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)

    def check_player_collision(self, player):
        return self.rect.colliderect(player.rect)
