import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from pygame.sprite import Group
from alien import Alien
from time import sleep
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption('Alien_Invasion')

        # сохранение экземпляров для хранения статистика и панели результатов
        self.ship = Ship(self)
        self.stats = GameStats(self)
        self.scoreboard = Scoreboard(self)

        self.play_button = Button(self, 'Play')

        # создаём список пуль для прорисовки каждого снаряда при проходе цикла
        self.bullets = Group()
        self.aliens = Group()
        self._create_fleet()

    def run_game(self):
        """Основной цикл игры(while... : all functions)"""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        """Обработка нажатий клавиш"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        """Проверка НАЖАТИЙ клавиш"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Проверка ОТПУСКАНИЙ клавиш"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Создание нового снаряда и включение его в группу bullets"""
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Обновляет позиции снарядов и уничтожает старые снаряды"""
        self.bullets.update()
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        # удаление снарядов за краем экрана
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions(collisions)

    def _check_bullet_alien_collisions(self, collisions):
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.scoreboard.prep_score()
            self.scoreboard.check_high_score()

        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            self.stats.level += 1
            self.scoreboard.prep_level()

    def _create_fleet(self):
        """Создание флота пришельцев, вычисление рядов"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        # по y
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # по x
        alien_width = alien.rect.width
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # создание рядов и строк
        for row_numbers in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_numbers)

    def _create_alien(self, alien_number, row_number):
        """Вычисление координат пришельца"""
        alien = Alien(self)
        alien_width = alien.rect.width
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _update_aliens(self):
        """Обновляет координаты всех пришельцев во флоте"""
        self._check_fleet_edges()
        self.aliens.update()
        # проверка столкновения пришельца с кораблём
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        # добрались ли пришельцы до нижнего края
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        """Реакция на достижение пришельцем правого края экрана"""
        for alien in self.aliens.sprites():
            # достиг правой/левой части экрана
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Изменение движения флота"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """Вызов функции если """
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.scoreboard.prep_ships()

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()
            sleep(0.5)
        else:
            self.stats.game_active = False
            # вывод указателя мыши
            pygame.mouse.set_visible(True)
            self.stats.level = 1

    def _check_aliens_bottom(self):
        """Проверка ниже/равен пришелец нижней стороне экрана"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _check_play_button(self, mouse_pos):
        """Новая игра если нажата кнопка PLAY"""
        # находится ли точка щелчка в пределах области 'кнопки'
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # сброс игровых настроек
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.scoreboard.prep_score()
            self.scoreboard.prep_level()
            self.scoreboard.prep_ships()

            # очистка списка пришельцев и снарядов
            self.aliens.empty()
            self.bullets.empty()

            # создание флота и размещение корабля в центре
            self._create_fleet()
            self.ship.center_ship()
            # скрытие указателя мыши
            pygame.mouse.set_visible(False)

    def _update_screen(self):
        """Обновление изображений на экране"""
        self.screen.blit(self.settings.phon, (0, 0))
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.scoreboard.show_score()
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()


ai = AlienInvasion()
ai.run_game()
