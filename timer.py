import pygame

TIMER_START = 60

class Timer:
    def __init__(self):
        self.time_left = TIMER_START
        self.last_tick = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        elapsed = (now - self.last_tick) // 1000
        if elapsed > 0:
            self.time_left = max(0, self.time_left - elapsed)
            self.last_tick = now

    def reset(self):
        self.time_left = TIMER_START
        self.last_tick = pygame.time.get_ticks()

    def is_time_up(self):
        return self.time_left <= 0
