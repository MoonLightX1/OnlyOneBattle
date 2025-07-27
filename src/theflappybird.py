# theflappybird.py
import pygame
import random

class FlappyBird:
    def __init__(self, x, arena_rect, width=20, rise_speed=5, move_speed=4):
        self.width = width
        self.height = 0
        self.full_height = random.randint(40, 160)
        self.x = float(x)
        self.rise_speed = rise_speed
        self.move_speed = move_speed
        self.arena_rect = arena_rect

        # Start at the bottom of the arena
        self.y = arena_rect.bottom
        self.rect = pygame.Rect(int(self.x), self.y, self.width, self.height)
        self.done = False

    def update(self):
        # Rise upward
        if self.height < self.full_height:
            self.height += self.rise_speed
            if self.height > self.full_height:
                self.height = self.full_height

        # Always move left while rising
        self.x -= self.move_speed

        # Update y and rect (rising from bottom up)
        self.y = self.arena_rect.bottom - self.height
        self.rect = pygame.Rect(int(self.x), int(self.y), self.width, self.height)

        # Remove if fully past the left wall
        if self.rect.right <= self.arena_rect.left:
            self.done = True

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)
        
    def check_player_collision(self, player):
        return self.rect.colliderect(player.rect)


def spawn_flappy_birf(vfx_list, x, y):
    birf = FlappyBird(x, y)
    vfx_list.append(birf)
    print(f"Spawned FlappyBird. Count: {len(vfx_list)}")