import time

import pygame
from bullet import Bullet
import math
from settings import Settings

class Tower(pygame.sprite.Sprite):
    def __init__(self, position, game):
        super().__init__()
        self.position = pygame.math.Vector2(position)
        self.game = game
        self.settings = Settings()

        self.image = None
        self.rect = None
        self.tower_range = 0
        self.damage = 0
        self.rate_of_fire = 0
        self.last_shot_time = pygame.time.get_ticks()
        self.level = 1
        self.original_image = self.image
        self.shoot_sound = pygame.mixer.Sound(self.settings.shoot_sound)

    def upgrade_cost(self):
        return 100 * self.level

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.is_hovered(mouse_pos):
            level_text = self.game.font.render(f"Level: {self.level}", True, (255, 255, 255))
            upgrade_cost_text = self.game.font.render(f"Upgrade: ${self.upgrade_cost()}", True, (255, 255, 255))

            level_text_pos = (self.position.x, self.position.y + 20)
            upgrade_cost_pos = (self.position.x, self.position.y + 40)

            screen.blit(level_text, level_text_pos)
            screen.blit(upgrade_cost_text, upgrade_cost_pos)

    def update(self, enemies, current_time, bullets_group):
        if current_time - self.last_shot_time > self.rate_of_fire:
            target = self.find_target(enemies)
            if target:
                self.rotate_towards_target(target)
                self.shoot(target, bullets_group)
                self.last_shot_time = current_time

    def is_hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def shoot(self, target, bullets_group):
        pass

    def rotate_towards_target(self, target):
        dx = target.position.x - self.position.x
        dy = target.position.y - self.position.y
        # Вычисляем угол в радианах
        angle_rad = math.atan2(dy, dx)
        # Преобразуем радианы в градусы
        angle_deg = math.degrees(angle_rad)
        angle_deg = -angle_deg - 90
        self.image = pygame.transform.rotate(self.original_image, angle_deg)
        self.rect = self.image.get_rect(center=self.position)

    def find_target(self, enemies):
        nearest_enemy = None
        min_distance = float('inf')
        for enemy in enemies:
            distance = self.position.distance_to(enemy.position)
            if distance < min_distance and distance <= self.tower_range:
                nearest_enemy = enemy
                min_distance = distance
        return nearest_enemy

    def upgrade(self):
        self.level += 1


class BasicTower(Tower):
    def __init__(self, position, game):
        super().__init__(position, game)
        self.image = pygame.image.load('tower_defence/assets/towers/basic_tower.png').convert_alpha()
        self.original_image = self.image
        self.rect = self.image.get_rect(center=self.position)
        self.tower_range = 150
        self.damage = 20
        self.rate_of_fire = 1000

    def shoot(self, target, bullets_group):
        self.shoot_sound.play()
        new_bullet = Bullet(self.position, target.position, self.damage, self.game)
        bullets_group.add(new_bullet)


class SniperTower(Tower):
    def __init__(self, position, game):
        super().__init__(position, game)
        self.image = pygame.image.load('tower_defence/assets/towers/sniper_tower.png').convert_alpha()
        self.image = pygame.transform.rotate(self.image, 90)
        self.original_image = self.image
        self.rect = self.image.get_rect(center=self.position)
        self.tower_range = 300
        self.damage = 40
        self.rate_of_fire = 2000

    def find_target(self, enemies):
        healthiest_enemy = None
        max_health = 0
        for enemy in enemies:
            if self.position.distance_to(enemy.position) <= self.tower_range and enemy.health > max_health:
                healthiest_enemy = enemy
                max_health = enemy.health
        return healthiest_enemy

    def shoot(self, target, bullets_group):
        self.shoot_sound.play()
        new_bullet = Bullet(self.position, target.position, self.damage, self.game)
        bullets_group.add(new_bullet)

class MoneyTower(Tower):
    """
    Класс, представляющий денежную башню в игре Tower Defense.
    Эта башня генерирует деньги для игрока с заданной скоростью.
    Описание:
    position: Позиция башни на игровом поле.
    game: Ссылка на текущую игру, позволяющая доступ к её ресурсам.
    image: Изображение башни.
    original_image: Оригинальное изображение для возможной трансформации.
    rect: Прямоугольник, определяющий размеры и положение башни.
    money_generation_rate: Количество денег, генерируемое за один интервал.
    generation_interval: Интервал времени (в миллисекундах) для генерации денег.
    last_generation_time: Время последней генерации денег.
    """
    def __init__(self, position, game):
        """
        Инициализация денежной башни
        """
        super().__init__(position, game)
        self.image = pygame.image.load('tower_defence/assets/towers/money_tower.png').convert_alpha()
        self.original_image = self.image
        self.rect = self.image.get_rect(center=self.position)
        self.money_generation_rate = 10  # Сколько денег генерируется
        self.generation_interval = 1000  # Интервал генерации в миллисекундах
        self.last_generation_time = pygame.time.get_ticks()

    def update(self, enemies, current_time, bullets_group):
        """
        Обновляет состояние башни, проверяя, должно ли произойти новое генерирование денег на основе текущего времени.
        Описание:
        enemies (Group): Группа врагов, с которыми взаимодействует башня.
        current_time (int): Текущее время в миллисекундах.
        bullets_group (Group): Группа пуль, выстреленных башней.
        """
        # Генерация денег с заданным интервалом
        if current_time - self.last_generation_time > self.generation_interval:
            self.generate_money()
            self.last_generation_time = current_time

    def generate_money(self):
        """
        Генерирует деньги для игрока, увеличивая его текущую сумму денег.
        """
        self.game.settings.starting_money += self.money_generation_rate
