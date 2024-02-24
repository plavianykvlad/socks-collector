from pygame import *
from random import randint
from time import time as time

img_back = 'kimnata.jpg'
img_hero = 'tazik.png'
img_enemy = 'sock1.png'

lost = 0
score = 0
max_lost = 5
life = 5

font.init()
font1 = font.SysFont('Arial', 80)
font2 = font.SysFont('Arial', 34)
win = font1.render('Шкарпетки зібрано, мама пишається тобою', True, (255, 255, 255))
lose = font1.render('Забагато втрачених шкарпеток', True, (255, 255, 255))

class GameSprite(sprite.Sprite):
    def init(self, player_image, player_x, player_y, size_x, size_y):
        sprite.Sprite.init(self)
        self.image = transform.sca;e(image.load(player_image),(size_x, size_y))
        self.speed = player_x
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

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(80, win_width - 80)
            lost += 1

win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(
    image.load(img_back), (
        win_width, win_height
    )
)

ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
monsters = sprite.Group()
for i in range(1, 7):
    monster = Enemy(img_enemy, randint(
        80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

finish = False
game = True

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:

                if not finish:
                    window.blit(background, (0, 0))
                    text = font2.render("Рахунок: " + str(score), 1, (255, 255, 255))
                    window.blit(text, (10, 20))
                    text_lost = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
                    window.blit(text_lost, (10, 50))

        ship.update()
        monsters.update()
        asteroids.update()
        bullets.update()

        ship.reset()
        monsters.draw(window)
        asteroids.draw(window)
        bullets.draw(window)
        if rel_time is True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render("Wait... reloading...", 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False
        
        collides = sprite.groupcolli
