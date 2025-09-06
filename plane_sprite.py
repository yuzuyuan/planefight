import random
import sys

import pygame

SCREEN_RECT = pygame.Rect(0, 0, 480, 700)
FRAME_PER_SEC = 60
CREATE_ENEMY_EVENT=pygame.USEREVENT
HERO_FIRE_EVENT=pygame.USEREVENT+1
class GameSprite(pygame.sprite.Sprite):
    def __init__(self,image_name,speed=1):
        super().__init__()
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self):
        self.rect.y+=self.speed

class Background(GameSprite):
    def __init__(self,is_alt=False):
        super().__init__("./images/images/Background.png")
        if is_alt:
            self.rect.y=-self.rect.height

    def update(self):
        super().update()
        if self.rect.y > SCREEN_RECT.height:
            self.rect.y=-self.rect.height

class Enemy(GameSprite):
    def __init__(self):
        super().__init__("./images/images/enemy1.png")
        self.speed=random.randint(1,2)
        self.rect.x=random.randint(0,SCREEN_RECT.width-self.rect.width)
        self.rect.bottom=0
        self.dying=False
        self.hp =1
        self.animation_frames = [
            pygame.image.load("./images/images/enemy1_down1.png").convert_alpha(),
            pygame.image.load("./images/images/enemy1_down2.png").convert_alpha(),
            pygame.image.load("./images/images/enemy1_down3.png").convert_alpha(),
            pygame.image.load("./images/images/enemy1_down4.png").convert_alpha()
        ]
        self.animation_index = 0
        self.animation_timer = 0

    def update(self):
        super().update()
        if self.rect.y > SCREEN_RECT.height:
            self.__del__()
        if self.dying:
            self.speed=0
            self.animation_timer+=1
            if self.animation_timer % 5 == 0:
                self.animation_index = (self.animation_index + 1) % len(self.animation_frames)
                self.image = self.animation_frames[self.animation_index]
            if self.animation_timer>20:
                self.kill()

    def die(self):
        self.animation_timer=0
        self.dying=True

    def __del__(self):
        self.kill()
    def hit(self):
        self.hp-=1
        if self.hp <=0:
            self.die()

class Hero(GameSprite):
    def __init__(self):
        super().__init__("./images/images/me1.png",0)
        self.rect.centerx=SCREEN_RECT.centerx
        self.rect.bottom=SCREEN_RECT.bottom-120
        self.bullets = pygame.sprite.Group()
        self.dying = False
        self.animation_frames = [
            pygame.image.load("./images/images/me_destroy_1.png").convert_alpha(),
            pygame.image.load("./images/images/me_destroy_2.png").convert_alpha(),
            pygame.image.load("./images/images/me_destroy_3.png").convert_alpha(),
            pygame.image.load("./images/images/me_destroy_4.png").convert_alpha()
        ]
        self.animation_index = 0
        self.animation_timer = 0
        self.game_over = False

    def update(self):
        self.rect.x+=self.speed
        if self.rect.x > SCREEN_RECT.width-self.rect.width:
            self.rect.x=SCREEN_RECT.width-self.rect.width
        elif self.rect.x<0:
            self.rect.x=0
        if self.dying:
            self.speed = 0
            self.animation_timer += 1
            if self.animation_timer % 5 == 0:
                self.animation_index = (self.animation_index + 1) % len(self.animation_frames)
                self.image = self.animation_frames[self.animation_index]
            if self.animation_timer > 20:
                self.kill()
                print("游戏结束")
                self.game_over = True


    def fire(self):
        for i in range(3):
            bullet=Bullet()
            bullet.rect.bottom=self.rect.y-i*20
            bullet.rect.centerx=self.rect.centerx
            self.bullets.add(bullet)

    def die(self):
        self.animation_timer=0
        self.dying=True
class Bullet(GameSprite):
    def __init__(self):
        super().__init__("./images/images/bullet1.png",-2)

    def update(self):
        super().update()
        if self.rect.bottom<0:
            self.kill()

    def __del__(self):
        pass
class Enemy2(Enemy):
    def __init__(self):
        GameSprite.__init__(self, "./images/images/enemy2.png")

        self.speed = random.randint(1, 2)
        self.rect.x = random.randint(0, SCREEN_RECT.width - self.rect.width)
        self.rect.bottom = 0
        self.hp = 8
        self.dying = False
        self.animation_frames = [
            pygame.image.load("./images/images/enemy2_down1.png").convert_alpha(),
            pygame.image.load("./images/images/enemy2_down2.png").convert_alpha(),
            pygame.image.load("./images/images/enemy2_down3.png").convert_alpha(),
            pygame.image.load("./images/images/enemy2_down4.png").convert_alpha()
        ]
        self.animation_index = 0
        self.animation_timer = 0


class Enemy3(Enemy):
    def __init__(self):

        GameSprite.__init__(self, "./images/images/enemy3_n1.png")
        

        self.speed = 1
        self.rect.x = random.randint(0, SCREEN_RECT.width - self.rect.width)
        self.rect.bottom = 0
        self.hp = 20
        self.dying = False
        self.animation_frames = [
            pygame.image.load("./images/images/enemy3_down1.png").convert_alpha(),
            pygame.image.load("./images/images/enemy3_down2.png").convert_alpha(),
            pygame.image.load("./images/images/enemy3_down3.png").convert_alpha(),
            pygame.image.load("./images/images/enemy3_down4.png").convert_alpha(),
            pygame.image.load("./images/images/enemy3_down5.png").convert_alpha(),
            pygame.image.load("./images/images/enemy3_down6.png").convert_alpha()
        ]
        self.animation_index = 0
        self.animation_timer = 0