from pygame import *
import pygame
from pygame.locals import *
import time
import random

# Screen initialize
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("sock-collector")

# Add this line to import clock
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
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx,
                        self.rect.top, 15, 20, -15)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(80, win_width - 80)
            lost += 1


# Background
kimnata = pygame.image.load("kimnata.jpg").convert_alpha()
kimnata = pygame.transform.scale(kimnata, (600, 600))

# Basket
tazik = pygame.image.load("tazik.png").convert_alpha()
tazik = pygame.transform.scale(tazik, (80, 80))
tazik_rect = tazik.get_rect()
tazik_rect.x = 260
tazik_rect.y = 500

# socks
socks_images = [
    pygame.image.load("sock1.png").convert_alpha(),
    pygame.image.load("sock2.png").convert_alpha(),
    pygame.image.load("sock3.png").convert_alpha()
]

for i in range(len(socks_images)):
    socks_images[i] = pygame.transform.scale(socks_images[i], (60, 60))

pygame.display.update()

# Movement of basket
exiting = False

score = 0

# Font
font = pygame.font.Font(None, 36)

# Timer
start_time = pygame.time.get_ticks()

# List to track collected socks
collected_socks = []

# List to track falling socks
falling_socks = []

# Timer event for adding new sock
ADD_SOCK_EVENT = pygame.USEREVENT + 1

# Start timer with 3 second interval
pygame.time.set_timer(ADD_SOCK_EVENT, 3000)

# Counter for number of socks added
sock_count = 0

# Index for current sock image
current_sock_index = 0

while not exiting:
    screen.blit(kimnata, (0, 0))
    
    # Draw timer
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
    timer_text = font.render("Час: " + str(elapsed_time), True, (255, 255, 255))
    screen.blit(timer_text, (10, 10))

    # Draw score
    score_text = font.render("Рахунок: " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (500, 10))

    # Update falling socks
    for sock_data in falling_socks:
        sock_data[1] += 5
        screen.blit(socks_images[sock_data[2]], (sock_data[0], sock_data[1]))

    for event in pygame.event.get():
        if event.type == QUIT:
            exiting = True
        elif event.type == ADD_SOCK_EVENT:
            if sock_count < 3:  # Add 3 socks
                xsock = random.randrange(50, 550)
                ysock = 20
                falling_socks.append([xsock, ysock, current_sock_index])
                sock_count += 1
                current_sock_index = (current_sock_index + 1) % len(socks_images)  # Move to next sock image

    keys = key.get_pressed()
    if keys[K_LEFT] and tazik_rect.x > 5:
        tazik_rect.x -= 5
    if keys[K_RIGHT] and tazik_rect.x < 515:
        tazik_rect.x += 5

    screen.blit(tazik, (tazik_rect.x, tazik_rect.y))

    # Check collision with sock
    for sock_data in falling_socks:
        if tazik_rect.colliderect((sock_data[0], sock_data[1], 60, 60)):
            if tuple(sock_data) not in collected_socks:  # Check if sock is already collected
                collected_socks.append(tuple(sock_data))  # Add collected sock to the list
                score += 1

                if score >= 10:
                    win_message = font.render("Мама тобою пишається", True, (255, 255, 255))
                    screen.blit(win_message, (150, 300))

    # Check if sock fell off the screen
    for sock_data in falling_socks:
        if sock_data[1] > 600:
            falling_socks.remove(sock_data)

    pygame.display.update()
    clock.tick(60)
