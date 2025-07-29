import pygame
import threading
import functools
import random
import math
from spinningballs import *
from theflappybird import *
from wave_splash import *
import numpy as np

class Button:
    def __init__(self, name, x, y, icon_path, width, height):
        self.name = name
        self.x = x
        self.y = y
        self.icon_path = icon_path
        self.width = width
        self.height = height
        self.icon = pygame.image.load(icon_path)
        self.icon = pygame.transform.scale(self.icon, (self.width, self.height))
    def is_clicked(self, mouse_pos):
        if self.x <= mouse_pos[0] <= self.x + self.width and self.y <= mouse_pos[1] <= self.y + self.height:
            return True
        return False
    def load_center(self, screen_width, y_coord):
        self.x = (screen_width - self.width) // 2
        self.y = y_coord
        self.icon = pygame.image.load(self.icon_path)
        self.icon = pygame.transform.scale(self.icon, (self.width, self.height))
    def load_right(self, screen_width, y_coord):
        self.x = screen_width - self.width - 15
        self.y = y_coord
        self.icon = pygame.image.load(self.icon_path)
        self.icon = pygame.transform.scale(self.icon, (self.width, self.height))
    def draw(self, screen):
        screen.blit(self.icon, (self.x, self.y))

class Text:
    def __init__(self, name, x, y, text, font, color):
        self.name = name
        self.x = x
        self.y = y
        self.text = text
        self.font = font
        self.color = color
        self.width = self.font.size(text)[0]
        self.height = self.font.size(text)[1]
        self.is_visible = False
        
    def draw(self, screen):
        text_surface = self.font.render(self.text, True, self.color)
        screen.blit(text_surface, (self.x, self.y))
        self.is_visible = True
        
    def undraw(self, screen):
        self.is_visible = False
        background_color = (0, 0, 0)
        pygame.draw.rect(screen, background_color, (self.x, self.y, self.width, self.height))
        
    def is_clicked(self, pos):
        if self.is_visible:
            if pos[0] >= self.x and pos[0] <= self.x + self.width:
                if pos[1] >= self.y and pos[1] <= self.y + self.height:
                    return True
        return False
    
    def draw_center(self, screen, screen_width, y_coord):
        text_surface = self.font.render(self.text, True, self.color)
        text_width, text_height = self.font.size(self.text)
        self.x = (screen_width - text_width) // 2
        self.y = y_coord
        screen.blit(text_surface, (self.x, self.y))
        self.is_visible = True
    def draw_bottom_right(self, screen, screen_width, y_coord=None):
        text_surface = self.font.render(self.text, True, self.color)
        text_width, text_height = self.font.size(self.text)
        if y_coord is None:
            self.y = screen.get_height() - text_height
        else:
            self.y = y_coord
        self.x = screen_width - text_width - 15
        screen.blit(text_surface, (self.x, self.y))
        self.is_visible = True

class SFX:
    def __init__(self, filename):
        pygame.mixer.init()
        self.original_sound = pygame.mixer.Sound(filename)
        self.sound_array = pygame.sndarray.array(self.original_sound)
        self.sample_rate = pygame.mixer.get_init()[0]
        self.loop_thread = None
        self._stop_loop = threading.Event()
        self.channel = None  # Track current channel

    def _play_loop(self, new_sound_array):
        new_sound = pygame.sndarray.make_sound(new_sound_array)
        while not self._stop_loop.is_set():
            self.channel = new_sound.play()
            length_ms = int(1000 * new_sound.get_length())
            elapsed = 0
            check_interval = 50  # ms
            while elapsed < length_ms:
                if self._stop_loop.is_set():
                    if self.channel:
                        self.channel.stop()
                    return
                pygame.time.wait(check_interval)
                elapsed += check_interval

    def play(self, min_pitch=1.0, max_pitch=1.0, loop=False, volume=1.0):
        pitch = random.uniform(min_pitch, max_pitch)
        if pitch == 1.0 and not loop and volume == 1.0:
            self.channel = self.original_sound.play()
            return

        sound_array = self.sound_array
        length = sound_array.shape[0]
        new_length = int(length / pitch)
        indices = np.linspace(0, length, new_length, endpoint=False)

        if len(sound_array.shape) == 1:
            new_sound_array = np.interp(indices, np.arange(length), sound_array).astype(np.int16)
        elif len(sound_array.shape) == 2:
            channels = sound_array.shape[1]
            new_sound_array = np.zeros((new_length, channels), dtype=np.int16)
            for ch in range(channels):
                new_sound_array[:, ch] = np.interp(indices, np.arange(length), sound_array[:, ch]).astype(np.int16)
        else:
            raise ValueError("Unsupported sound array shape.")

        # Apply volume scaling
        new_sound_array = (new_sound_array * volume).clip(-32768, 32767).astype(np.int16)

        if loop:
            self.stop()  # Stop any existing loop
            self._stop_loop.clear()
            self.loop_thread = threading.Thread(target=self._play_loop, args=(new_sound_array,))
            self.loop_thread.daemon = True
            self.loop_thread.start()
        else:
            new_sound = pygame.sndarray.make_sound(new_sound_array)
            new_sound.set_volume(volume)
            self.channel = new_sound.play()

    def stop(self):
        self._stop_loop.set()
        if self.loop_thread and self.loop_thread.is_alive():
            self.loop_thread.join(timeout=0.1)
        self.loop_thread = None

        # Stop any currently playing channel
        if self.channel and self.channel.get_busy():
            self.channel.stop()
            self.channel = None

        self.original_sound.stop()

def delayed_call(delay, func, *args, **kwargs):
    wrapped = functools.partial(func, *args, **kwargs) # I FUCKING HATE THREADS SO FUCKING MUCH AHHHHHHHHHHHHH
    timer = threading.Timer(delay, wrapped)
    timer.daemon = True
    timer.start()
    return timer

class TiledTransition:
    def __init__(self, frame_paths, screen_size, tile_size=(32, 32), frame_delay=5, extra_delay=5, reverse=False):
        self.frames = [pygame.transform.scale(pygame.image.load(p).convert_alpha(), tile_size) for p in frame_paths]
        if reverse:
            self.frames = list(reversed(self.frames))
        self.tile_w, self.tile_h = tile_size
        self.screen_w, self.screen_h = screen_size
        self.cols = (self.screen_w // self.tile_w) + 1
        self.rows = (self.screen_h // self.tile_h) + 1
        self.frame_delay = frame_delay
        self.extra_delay = extra_delay  # extra delay on last frame
        self.current_frame = 0
        self.counter = 0
        self.done = False

    def update(self):
        self.counter += 1
        if self.counter >= self.frame_delay:
            self.counter = 0
            if self.current_frame == len(self.frames) - 1:
                # On last frame, wait extra_delay frames before finishing
                if hasattr(self, 'extra_counter'):
                    self.extra_counter += 1
                else:
                    self.extra_counter = 1
                if self.extra_counter >= self.extra_delay:
                    self.done = True
            else:
                self.current_frame += 1

    def draw(self, screen):
        if self.current_frame < len(self.frames):
            frame = self.frames[self.current_frame]
            for y in range(self.rows):
                for x in range(self.cols):
                    screen.blit(frame, (x * self.tile_w, y * self.tile_h))

    def is_done(self):
        return self.done

#for battle shit
def draw_status_texts(screen, font, player, boss, remaining_bullets, equipped_item, stage_lvl, time_left_minutes):
    timeleft = f"Time Left: {time_left_minutes:.2f} min"
    if stage_lvl == 1:
        timeleft == "No time limit for this battle."
    if stage_lvl == 8 or stage_lvl == 7 or stage_lvl == 2:
        stage_lvl = 2
        timeleft == "No time limit for this battle."
    if stage_lvl == 5 or stage_lvl == 4 or stage_lvl == 3:
        stage_lvl = 3
    texts = [
        f"Your health: {player.health}",
        f"Boss's health: {boss.health}",
        f"Bullets Left: {remaining_bullets}",
        f"Equipped Item: {equipped_item}",
        f"Stage: {stage_lvl}",
        f"{timeleft}"
    ]

    x = 1557
    y = 545
    line_height = font.get_height() + 5

    for i, text in enumerate(texts):
        text_surface = font.render(text, True, (255, 255, 255))
        screen.blit(text_surface, (x, y + i * line_height))

# def boss_attack_loop(vfx_list, wave_splash_list, boss, arena_rect, flappybirds):
#     try:
#         action = random.randint(1, 3)
#         print(f"[boss_attack_loop] Action chosen: {action}")
#         if action == 1:
#             print("Boss uses: Wave Splash")
#             splash_width = 20
#             gap = 6
#             spacing = splash_width + gap  # 26 px between start of one splash to next

#             start_x = boss.rect.left - 30
#             for height_rank in range(8):
#                 splash_x = start_x + height_rank * spacing
#                 wave_splash_list.append(WaveSplashRect(splash_x, arena_rect, height_rank, width=splash_width))
#         elif action == 2:
#             print("Boss uses: Flappy Birf")
#             flappybirds.append(
#                     FlappyBird(x=boss.rect.centerx, arena_rect=arena_rect)
#                 )
#         elif action == 3:
#             print("Boss uses: Spinning Balls")
#             angles = [i for i in range(30, 360, 30)]  # Skips top (0 degrees)
#             for angle in angles:
#                 rad = math.radians(angle)
#                 speed = 5
#                 dx = math.cos(rad) * speed
#                 dy = math.sin(rad) * speed
#                 spawn_x = boss.rect.centerx
#                 spawn_y = boss.rect.centery
#                 spinning_ball = SpinningBall(spawn_x, spawn_y, dx, dy, arena_rect)
#                 vfx_list.append(spinning_ball)
#     except Exception as e:
#         print(f"Exception in boss_attack_loop: {e}")

#     # Schedule the next attack after 5 seconds
#     delayed_call(5.0, boss_attack_loop, vfx_list, wave_splash_list, boss, arena_rect, flappybirds)


def shift_pitch(sound, pitch_factor):
    arr = pygame.sndarray.array(sound)

    # Resample: new length = old / pitch_factor
    indices = np.round(np.arange(0, len(arr), pitch_factor)).astype(int)
    indices = indices[indices < len(arr)]  # Avoid out-of-bounds
    new_arr = arr[indices]

    return pygame.sndarray.make_sound(new_arr.copy())