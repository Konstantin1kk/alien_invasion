import pygame


class Settings:
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (255, 255, 0)
        self.phon = pygame.image.load('images/space_wallpaper.png')

        # корабль
        self.ship_speed = 1.5
        self.ship_limit = 2

        # пуля
        self.bullet_speed = 1
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_allowed = 3

        # alien
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        self.fleet_direction = 1
        self.alien_points = 50
        self.score_scale = 1.5

        # темп ускорения игры
        self.speedup_scale = 1.1

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Инициализирует настройки, изменяющиеся в ходе игры"""
        self.ship_speed = 4.0 #1.5
        self.bullet_speed = 5.0 # 3
        self.alien_speed = 1 # 03
        self.score_scale = 1.5

        self.fleet_direction = 1

    def increase_speed(self):
        """Увеличение настроек скорости"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
