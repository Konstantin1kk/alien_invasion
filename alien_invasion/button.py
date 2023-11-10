import pygame
from pygame import font


class Button:
    def __init__(self, ai_game, msg):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # размеры и свойства кнопки
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 255)
        self.text_color = (255, 255, 255)
        self.font = font.SysFont(None, 48)

        # прямоугольник кнопки и выравнивание по центру экрана
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        self._prep_msg(msg)

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def _prep_msg(self, msg):
        """Получает сообщение(msg) и выводит его в центре прямоугольника 'кнопки' """
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

