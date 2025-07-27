import random
import pygame

class ParticleEffect:
    def __init__(self, x, y, size_multiplier=1):
        self.particles = []
        for _ in range(10 * size_multiplier):  # more particles for bigger explosion
            vx = random.randint(-5 * size_multiplier, 5 * size_multiplier)
            vy = random.randint(-5 * size_multiplier, -1 * size_multiplier)
            radius = random.randint(4, 8) * size_multiplier
            self.particles.append([[x, y], [vx, vy], radius])

    def update(self):
        for p in self.particles:
            p[0][0] += p[1][0]
            p[0][1] += p[1][1]
            p[2] -= 0.3 * (p[2] / max(p[2], 1))  # scale shrink speed by size

        self.particles = [p for p in self.particles if p[2] > 0]

    def draw(self, screen):
        for p in self.particles:
            pygame.draw.circle(screen, (255, 180, 80), (int(p[0][0]), int(p[0][1])), int(p[2]))

    def is_done(self):
        return len(self.particles) == 0