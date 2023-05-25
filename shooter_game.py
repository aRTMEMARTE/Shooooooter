from pygame import *
from random import *
from time import time as timer

mixer.init()
font.init()

window = display.set_mode((700,500))
display.set_caption("Шутер")
background = transform.scale(image.load("galaxy.jpg"), (700, 500))
player = transform.scale(image.load('rocket.png'), (100, 110))

clock = time.Clock()
FPS = 60
lost = 0
score = 0
life = 3
rel_time = False
num_fire = 0

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x >= 0:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x <= 630:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("bullet.png", rocket.rect.centerx, rocket.rect.top, 15, 20, 15)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.x = randint(80, 620)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


mixer.music.load('space.ogg')
mixer.music.play()

r_fire = mixer.Sound('fire.ogg')

rocket = Player('rocket.png',50, 410, 80, 90, 10)
monsters = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()

for i in range(1,6):
    monster = Enemy("ufo.png", randint(80, 620), -40, 80, 50, 2)
    monsters.add(monster)

for i in range(1,3):
    asteroid = Enemy("asteroid.png", randint(80, 620), -40, 80, 50, 2)
    asteroids.add(asteroid)




font2 = font.SysFont('Arial', 36)
font10 = font.SysFont('Arial', 80)

finish = False
action = True
while action:
    for even in event.get():
        if even.type == QUIT:
            action = False
        if even.type == KEYDOWN:
            if even.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    r_fire.play()
                    rocket.fire()

                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True

                
    if finish != True:
        window.blit(background, (0,0))
        rocket.update()
        monsters.update()
        bullets.update()
        asteroids.update()

        sprites_list=sprite.groupcollide(monsters, bullets, True, True)
        for s in sprites_list:
            score += 1
            monster = Enemy("ufo.png", randint(80, 620), -40, 80, 50, 2)
            monsters.add(monster)
        
        if sprite.spritecollide(rocket, monsters, False) or sprite.spritecollide(rocket, asteroids, False):
            sprite.spritecollide(rocket, monsters, True)
            sprite.spritecollide(rocket, asteroids, True)
            life -= 1
        
        if life == 0 or lost >= 20:
            lose = font2.render('YOU LOSE', True, (200, 27, 27))
            window.blit(lose, (350, 250))
            finish = True

        if score == 10:
            win = font2.render('YOU WIN', True, (50, 199, 207))
            window.blit(win, (350, 250))
            finish = True

        text_lose = font2.render('ПРОПУЩЕНО:' + str(lost), 1, (255,255, 255))
        window.blit(text_lose, (50,50))
        text_counter = font2.render('СЧЁТ:' + str(score),1, (255,255, 255))
        window.blit(text_counter, (50, 100))
        
        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (150, 0, 0)
        
        text_life = font10.render(str(life), 1, life_color)
        window.blit(text_life, (650, 100))

        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload1 = font2.render('Wait, reload...', 1 , (150, 0, 0))
                window.blit(reload1, (260, 460))
            else:
                num_fire = 0
                rel_time = False

        rocket.reset()
        
    clock.tick(FPS)
    display.update()