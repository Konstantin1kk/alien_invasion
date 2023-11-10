import pygame


class GameStats:
    def __init__(self, ai_game):
        pygame.init()
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active = True
        self.high_score = 0
        self.level = 1

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
