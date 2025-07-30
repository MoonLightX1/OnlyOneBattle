import pygame
import time

from bullets import *
from vfx import *
from util import SFX, resource_path

class Player:
    def __init__(self, spawn_x, spawn_y, width, height, arena_rect):
        self.speed = 5
        self.jump_power = -20
        self.gravity = 1
        self.velocity_y = 0
        self.screen_shake = 0 
        self.is_jumping = False
        self.image = resource_path("data/artwork/playerstar.png").convert_alpha()
        self.original_image = self.image  # for flipping if needed
        self.rect = self.image.get_rect(topleft=(spawn_x, spawn_y))
        self.last_damage_time = 0
        self.health = 125
        self.damage_cooldown = 0.1 
        self.arena = arena_rect
        self.current_weapon = "gun" 

        self.charging = False
        self.charge_power = 5
        self.charge_max = 20
        self.charge_start_time = 0
        
        self.facing_right = False

        # Shooting
        self.bullets = []
        self.bullets_fired = 0
        self.max_bullets = 3
        self.reload_time = 60  # frames
        self.reload_counter = 0
        self.direction = 1
        
        # Ammo system
        self.max_ammo = 3
        self.ammo = self.max_ammo
        self.reload_cooldown = 1000  # milliseconds
        self.last_reload_time = 0
        self.reloading = False
        
        self.jumpSFX = SFX("data/sounds/jump_SFX.mp3")
        self.hurtSFX = SFX("data/sounds/damage sfx.mp3")
        self.deathSFX = SFX("data/sounds/death sfx.mp3")
        self.chargeSFX = SFX("data/sounds/charge sfx.mp3")
        self.shootSFX = SFX("data/sounds/shoot sfx.mp3")
        self.chargereleaseSFX = SFX("data/sounds/charge release sfx.mp3")

    def handle_input(self, keys):
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
            self.direction = -1
        if keys[pygame.K_d]:
            self.rect.x += self.speed
            self.direction = 1

    def jump(self):
        if not self.is_jumping:
            self.jumpSFX.play(0.6, 1.5, False, 0.6)
            self.velocity_y = self.jump_power
            self.is_jumping = True
            
    def take_damage(self, amount):
        self.hurtSFX.play(0.6, 1.5, False, 0.5)
        now = time.time()
        if now - self.last_damage_time >= self.damage_cooldown:
            self.health -= amount
            self.last_damage_time = now
            print(f"Player took {amount} damage! Health now: {self.health}")
            if self.health <= 0:
                self.deathSFX.play(1,1,False,1.5)
                self.chargeSFX.stop()
                self.shootSFX.stop()
                self.health = 0
    
    def start_charging(self):
        self.charging = True
        self.charge_start_time = pygame.time.get_ticks()
        self.chargeSFX.play(0.6,1.5,True,0.8)

    def stop_charging_and_shoot(self, vfx_list):
        if not self.charging:
            return
        self.charging = False
        self.chargereleaseSFX.play(0.6,1.5,False,0.7)
        self.shootSFX.play(1,1,False,1)
        self.chargeSFX.stop()

        if self.ammo <= 0:
            return

        self.ammo -= 1

        time_held = pygame.time.get_ticks() - self.charge_start_time
        charge = 5 + (15 * (time_held / 1000))  # from 5 to 20
        charge = min(charge, self.charge_max)
        
        print(f"Charged: {charge:.2f} Power | {self.ammo} Bullets Left")

        mouse_x, mouse_y = pygame.mouse.get_pos()
        bullet = Bullet(self.rect.centerx, self.rect.centery, mouse_x, mouse_y, "data/artwork/longbullet.png", power=charge)
        vfx_list.append(bullet)

        # recoil
        #sucks in this yummy code
        dx = mouse_x - self.rect.centerx
        dy = mouse_y - self.rect.centery
        dist = math.hypot(dx, dy)
        if dist == 0:
            dist = 1
        recoil_strength = charge * 0.8 
        recoil_vx = -(dx / dist) * recoil_strength
        recoil_vy = -(dy / dist) * recoil_strength

        self.rect.x += recoil_vx
        self.rect.y += recoil_vy
        
        vfx_list.append(ParticleEffect(self.rect.centerx, self.rect.centery))

        # Add dust effect at feet
        for _ in range(3):
            vfx_list.append(ParticleEffect(self.rect.centerx, self.rect.bottom))

        # Apply screen shake (scaled to charge)
        self.screen_shake = int(charge * 0.6)  # max ~12 px

    def die(self):
        print("Player has died.")
        # pretty self explanatory unless dumb

    def apply_gravity(self):
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        if self.rect.bottom >= self.arena.bottom:
            self.rect.bottom = self.arena.bottom
            self.velocity_y = 0
            self.is_jumping = False

        if self.rect.top < self.arena.top:
            self.rect.top = self.arena.top
            self.velocity_y = 0

    def constrain_to_arena(self):
        if self.rect.left < self.arena.left:
            self.rect.left = self.arena.left
        if self.rect.right > self.arena.right:
            self.rect.right = self.arena.right

    def shoot(self, vfx_list):
        if self.bullets_fired < self.max_bullets:
            # Get mouse position at time of firing
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Create bullet toward mouse
            bullet = Bullet(self.rect.centerx, self.rect.centery, mouse_x, mouse_y, power=20)
            self.bullets.append(bullet)
            self.bullets_fired += 1

            # Apply recoil based on bullet direction
            recoil_dir = -1 if bullet.vx > 0 else 1
            self.rect.x += recoil_dir * 10

            # Add visual effect
            vfx_list.append(ParticleEffect(bullet.rect.centerx, bullet.rect.centery))

        
    def reload_check(self):
        if self.bullets_fired >= self.max_bullets:
            self.reload_counter += 1
            if self.reload_counter >= self.reload_time:
                self.bullets_fired = 0
                self.reload_counter = 0

    def update(self, keys, walls, vfx_list):
        self.handle_input(keys)
        self.apply_gravity()
        self.constrain_to_arena()
        self.reload_check()

        for bullet in self.bullets:
            bullet.update(walls, vfx_list)
        self.bullets = [b for b in self.bullets if b.alive]
        if keys[pygame.K_LEFT]:
            self.facing_right = False
        elif keys[pygame.K_RIGHT]:
            self.facing_right = True

    def stop_current_sfx(self):
        self.chargeSFX.stop()
        self.shootSFX.stop()
        self.chargereleaseSFX.stop()

    def draw(self, screen):
        # Flip if facing left
        image_to_draw = pygame.transform.flip(self.original_image, not self.facing_right, False)
        screen.blit(image_to_draw, self.rect)

        for bullet in self.bullets:
            bullet.draw(screen)
    
    def handle_reload(self):
        if self.ammo <= 0 and not self.reloading:
            self.reloading = True
            self.last_reload_time = pygame.time.get_ticks()

        if self.reloading:
            now = pygame.time.get_ticks()
            if now - self.last_reload_time >= self.reload_cooldown:
                self.ammo = self.max_ammo
                self.reloading = False
    
    def get_charge_level(self):
        if not self.charging:
            return 0, (0, 0, 0)  # No charge, no color

        time_held = pygame.time.get_ticks() - self.charge_start_time
        charge = 5 + (15 * (time_held / 1000))  # scale from 5 to 20
        charge = min(charge, self.charge_max)

        # Compute color based on charge level
        if charge < 8:
            color = (100, 255, 100) 
        elif charge < 11:
            color = (220, 220, 80) 
        elif charge < 15:
            color = (255, 140, 50)  
        else:
            color = (255, 60, 60)  

        return (charge - 5) / 15, color  # Normalize between 0-1