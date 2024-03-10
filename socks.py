from pygame import *
import pygame
from pygame.locals import *
import time
import random

# Ініціалізація екрану
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("sock-collector")

#  годинник
clock = pygame.time.Clock()

class GameSprite(sprite.Sprite):
    def __init__(self, player_image,
                player_x, player_y,
                size_x, size_y,
                player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(
            image.load(player_image), (
                size_x, size_y
            ))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        screen.blit(self.image, (
            self.rect.x, self.rect.y
        ))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 515:
            self.rect.x += self.speed

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 600 or self.rect.x < 0 or self.rect.x > 600:
            self.rect.y = 0
            self.rect.x = random.randint(0, 600)


# Фон
kimnata = pygame.image.load("kimnata.jpg").convert_alpha()
kimnata = pygame.transform.scale(kimnata, (600, 600))

# Кошик
tazik = pygame.image.load("tazik.png").convert_alpha()
tazik = pygame.transform.scale(tazik, (80, 80))
tazik_rect = tazik.get_rect()
tazik_rect.x = 260
tazik_rect.y = 500

# Шкарпетки
socks_images = [
    pygame.image.load("sock1.png").convert_alpha(),
    pygame.image.load("sock2.png").convert_alpha(),
    pygame.image.load("sock4.png").convert_alpha()
]

for i in range(len(socks_images)):
    socks_images[i] = pygame.transform.scale(socks_images[i], (60, 60))

pygame.display.update()

# Рух кошика
exiting = False

score = 0

# Шрифт
font = pygame.font.Font(None, 36)

# Таймер
start_time = pygame.time.get_ticks()
sock_spawn_time = pygame.time.get_ticks()

# Список для відстеження зібраних шкарпеток
collected_socks = []

# Список для відстеження падаючих шкарпеток
falling_socks = []

# Лічильник для кількості доданих шкарпеток
sock_count = 0

# Індекс поточного зображення шкарпетки
current_sock_index = 0

while not exiting:
    screen.blit(kimnata, (0, 0))
    
    # Відображення таймера
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
    timer_text = font.render("Час: " + str(elapsed_time), True, (0, 0, 0))
    screen.blit(timer_text, (10, 10))

    # Відображення рахунку
    score_text = font.render("Рахунок: " + str(score), True, (0, 0, 0))
    screen.blit(score_text, (450, 10))

    # Оновлення падаючих шкарпеток
    for sock_data in falling_socks:
        sock_data[1] += 5
        screen.blit(socks_images[sock_data[2]], (sock_data[0], sock_data[1]))

    # Створення нових шкарпеток з інтервалом 5 секунд
    current_time = pygame.time.get_ticks()
    if current_time - sock_spawn_time >= 3000:
        xsock = random.randrange(50, 550)
        ysock = 20
        falling_socks.append([xsock, ysock, current_sock_index])
        current_sock_index = (current_sock_index + 1) % len(socks_images)
        sock_spawn_time = current_time

    for event in pygame.event.get():
        if event.type == QUIT:
            exiting = True

    keys = key.get_pressed()
    if keys[K_LEFT] and tazik_rect.x > 5:
        tazik_rect.x -= 5
    if keys[K_RIGHT] and tazik_rect.x < 515:
        tazik_rect.x += 5

    screen.blit(tazik, (tazik_rect.x, tazik_rect.y))

    # Перевірка колізії зі шкарпеткою та кошиком
    for sock_data in falling_socks:
        sock_rect = pygame.Rect(sock_data[0], sock_data[1], 60, 60)
        if tazik_rect.colliderect(sock_rect):
            if tuple(sock_data) not in collected_socks:
                collected_socks.append(tuple(sock_data))
                score += 1
                falling_socks.remove(sock_data)
                if score >= 10:
                    win_message = font.render("Мама тобою пишається", True, (255, 255, 255))
                    screen.blit(win_message, (150, 300))
    
    # Оновлення позиції падаючих шкарпеток та обробка телепортації
    for sock_data in falling_socks:
        if sock_data[1] > 600 or sock_data[0] < 0 or sock_data[0] > 600:
            sock_data[1] = 0
            sock_data[0] = random.randint(0, 600)

    pygame.display.update()
    clock.tick(60)
