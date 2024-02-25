from pygame import *
import pygame
from pygame.locals import *
import time
import random


clock = pygame.time.Clock()
x=260
y=500
#Screen initialize
pygame.init()
pygame.font.init()
screen=pygame.display.set_mode((600,600))
pygame.display.set_caption("sock")

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
        window.blit(self.image, (
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



#Background
kimnata=pygame.image.load("kimnata.jpg").convert_alpha()
kimnata=pygame.transform.scale(kimnata,(600,600))
screen.blit(kimnata,(0,0))

#Basket
tazik=pygame.image.load("tazik.png").convert_alpha()
tazik=pygame.transform.scale(tazik,(80,80))

#sock
sock=pygame.image.load("sock1.png").convert_alpha()
sock= pygame.transform.scale(sock,(60,60))

#screen.blit(sock,(290,20))
pygame.display.update()

#Movement of basket
ychange=0
xchange=0
exiting=False


xsock = random.randrange(50,550)
ysock = 20
while not exiting:
    screen.blit(kimnata,(0,0))
    if ysock<550:
        ysock += 5
        clock.tick(60)
        screen.blit(sock,(xsock,ysock))

    else:
        ysock=20
        xsock = random.randrange(50,550)
        ysock=ysock+ychange
        clock.tick(60)
        screen.blit(sock,(xsock,ysock))

    for event in pygame.event.get():
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

        x=x+xchange
        

        screen.blit(tazik,(x,y))

    pygame.display.update()
    clock.tick(60)
