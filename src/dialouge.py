import pygame
import time
import textwrap
from util import *

class DialogueBox:
    def __init__(self, text, author, font, screen, width, height,
                 y_offset=50, type_time=3, stay_time=2,
                 char_sound=None, pitch_factor=1.0):
        self.text = text
        self.author = author
        self.font = font
        self.screen = screen
        self.screen_rect = screen.get_rect()
        

        self.width = width
        self.height = height
        self.y_offset = y_offset
        self.x = self.screen_rect.centerx - self.width // 2
        self.y = self.screen_rect.bottom - self.height - self.y_offset
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.type_time = type_time
        self.stay_time = stay_time
        self.start_time = time.time()
        self.finished_typing = False
        self.remove_after = None

        self.author_color = (100, 200, 255)
        self.text_color = (255, 255, 255)
        self.bg_color = (20, 20, 20, 220)

        self.total_chars = len(text)
        self.chars_per_second = self.total_chars / self.type_time if self.type_time > 0 else 50
        self.visible_chars = 0
        self.last_word_index = -1

        self.padding = 12
        self.line_spacing = 6

        self.char_sound = char_sound
        self.pitch_factor = pitch_factor
        self.last_char_index = -1  # Tracks last char sound was played for

    def play_word_sound(self):
        if self.word_sound:
            pitched = shift_pitch(self.word_sound, self.pitch_factor)
            pitched.play()
            

    def update(self):
        if self.finished_typing:
            if time.time() >= self.remove_after:
                return True
            return False

        elapsed = time.time() - self.start_time
        new_visible = int(self.chars_per_second * elapsed)
        new_visible = min(new_visible, self.total_chars)

        # Play sound for each newly revealed character
        if new_visible > self.last_char_index:
            for i in range(self.last_char_index + 1, new_visible):
                char = self.text[i]
                if char != ' ' and self.char_sound:
                    pitched = shift_pitch(self.char_sound, self.pitch_factor)
                    pitched.play()
            self.last_char_index = new_visible - 1

        self.visible_chars = new_visible

        if self.visible_chars >= self.total_chars:
            self.finished_typing = True
            self.remove_after = time.time() + self.stay_time

        return False
    def draw(self):
        pygame.draw.rect(self.screen, self.bg_color, self.rect, border_radius=10)

        author_surface = self.font.render(self.author, True, self.author_color)
        self.screen.blit(author_surface, (self.x + self.padding, self.y + self.padding))

        text_start_y = self.y + self.padding + author_surface.get_height() + self.line_spacing
        visible_text = self.text[:self.visible_chars]
        wrapped_lines = textwrap.wrap(visible_text, width=45)

        for line in wrapped_lines:
            line_surf = self.font.render(line, True, self.text_color)
            self.screen.blit(line_surf, (self.x + self.padding, text_start_y))
            text_start_y += line_surf.get_height() + self.line_spacing
            
class DialogueManager:
    def __init__(self, font, screen, width=600, height=130, y_offset=50):
        self.font = font
        self.screen = screen
        self.width = width
        self.height = height
        self.y_offset = y_offset
        self.dialogue_queue = []
        self.current_dialogue = None

    def queue_dialogue(self, text, author, type_time=3, stay_time=2,
                   char_sound=None, pitch_factor=1.0):
        self.dialogue_queue.append((text, author, type_time, stay_time, char_sound, pitch_factor))
        # oh my fucking god did i have a whole ass queue system but i did the timings myself...
    def update(self):
        if self.current_dialogue is None and self.dialogue_queue:
            text, author, type_time, stay_time, char_sound, pitch_factor = self.dialogue_queue.pop(0)
            self.current_dialogue = DialogueBox(text, author, self.font, self.screen,
                                                self.width, self.height, self.y_offset,
                                                type_time, stay_time,
                                                char_sound, pitch_factor)
        if self.current_dialogue:
            done = self.current_dialogue.update()
            if done:
                self.current_dialogue = None

    def draw(self):
        if self.current_dialogue:
            self.current_dialogue.draw()

    def is_active(self):
        return self.current_dialogue is not None
