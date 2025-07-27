import pygame

class GiantLazer:
    def __init__(self, boss, arena_rect, width=24, color=(255, 0, 0), rise_speed=12, sweep_speed=7):
        self.arena_rect = arena_rect
        self.color = color
        self.width = width
        self.rise_speed = rise_speed
        self.sweep_speed = sweep_speed

        # Start from the ground
        self.x = boss.rect.centerx - self.width // 2 + 80
        self.top_y = arena_rect.bottom  # start from the bottom
        self.target_top_y = arena_rect.top  # rise to top of arena
        self.height = 0

        self.state = "rising"  # rising -> sweeping -> done
        self.finished = False  # flag to mark for removal

    def update(self):
        if self.state == "rising":
            self.top_y -= self.rise_speed
            if self.top_y <= self.target_top_y:
                self.top_y = self.target_top_y
                self.height = self.arena_rect.bottom
                self.state = "sweeping"

        elif self.state == "sweeping":
            self.x -= self.sweep_speed
            if self.x <= self.arena_rect.left + 60:
                self.x = self.arena_rect.left + 60
                self.state = "done"

        elif self.state == "done":
            # Mark laser as finished so it can be removed
            self.finished = True

    def draw(self, screen):
        if self.state == "rising":
            dynamic_height = self.arena_rect.bottom - self.top_y
            rect = pygame.Rect(self.x, self.top_y, self.width, dynamic_height)
        else:
            rect = pygame.Rect(self.x, self.top_y, self.width, self.height)
        pygame.draw.rect(screen, self.color, rect)

    def check_player_collision(self, player):
        if self.state in ["sweeping", "done"]:
            rect = pygame.Rect(self.x, self.top_y, self.width, self.height)
            return rect.colliderect(player.rect)
        return False
