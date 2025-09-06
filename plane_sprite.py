import random
import pygame
from powerups import PiercingShotPowerUp, SlowingShotPowerUp
from base_sprites import GameSprite, Bullet 

# 屏幕大小
SCREEN_RECT = pygame.Rect(0, 0, 480, 700)
# 物资区宽度
SUPPLY_ZONE_WIDTH = 120
# 帧率
FRAME_PER_SEC = 60
# 创建敌机的定时器事件
CREATE_ENEMY_EVENT = pygame.USEREVENT
# 英雄发射子弹的定时器事件
HERO_FIRE_EVENT = pygame.USEREVENT + 1


class Background(GameSprite):
    """游戏背景精灵"""
    def __init__(self, is_alt=False):
        super().__init__("./images/images/background.png")
        if is_alt:
            self.rect.y = -self.rect.height

    def update(self):
        super().update()
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -self.rect.height


class Hero(GameSprite):
    """英雄精灵"""
    def __init__(self):
        super().__init__("./images/images/me1.png", 0)
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom - 120
        self.bullets = pygame.sprite.Group()
        self.level = 1
        self.mask = pygame.mask.from_surface(self.image)

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
        if self.active_powerup:
            self.active_powerup.update()
        self.rect.x += self.speed
        if self.rect.left < 0: self.rect.left = 0
        elif self.rect.right > SCREEN_RECT.width: self.rect.right = SCREEN_RECT.width
        if self.dying:
            self.speed = 0
            self.animation_timer += 1
            if self.animation_timer % 5 == 0:
                if self.animation_index < len(self.animation_frames) - 1:
                    self.animation_index += 1
                    self.image = self.animation_frames[self.animation_index]
                    self.mask = pygame.mask.from_surface(self.image)
                else:
                    self.kill()
                    self.game_over = True

    def fire(self):
        if not self.dying:
            if self.active_powerup:
                self.active_powerup.fire(self.bullets)
            else:
                for i in range(self.level):
                    bullet = Bullet()
                    bullet.rect.bottom = self.rect.y - i * 20
                    bullet.rect.centerx = self.rect.centerx
                    self.bullets.add(bullet)

    def upgrade(self):
        if self.level < 5: self.level += 1

    def die(self):
        if not self.dying:
            self.dying = True
            self.animation_timer = 0

class FriendPlane(GameSprite):
    """友机精灵"""
    def __init__(self):
        super().__init__("./images/images/life.png", 0)
        self.mask = pygame.mask.from_surface(self.image)

    def fire(self, bullets_group):
        if self.active_powerup:
            self.active_powerup.fire(bullets_group)
        else:
            bullet = Bullet()
            bullet.rect.bottom = self.rect.y
            bullet.rect.centerx = self.rect.centerx
            bullets_group.add(bullet)
    
    def update(self):
        if self.active_powerup:
            self.active_powerup.update()


class Enemy(GameSprite):
    """敌机精灵基类"""
    def __init__(self, image_name, speed, hp, score, morale_penalty, animation_frames):
        super().__init__(image_name, speed)
        self.hp = hp
        self.score = score
        self.morale_penalty = morale_penalty
        self.initial_speed = speed
        self.slow_timer = 0
        self.rect.bottom = 0
        self.rect.x = random.randint(SUPPLY_ZONE_WIDTH, SCREEN_RECT.width - self.rect.width)
        self.mask = pygame.mask.from_surface(self.image)

        self.dying = False
        self.animation_frames = [pygame.image.load(frame).convert_alpha() for frame in animation_frames]
        self.animation_index = 0
        self.animation_timer = 0

    def update(self):
        if self.slow_timer > 0:
            self.speed = self.initial_speed * 0.5
            self.slow_timer -= 1
        else:
            self.speed = self.initial_speed
        
        super().update()
        
        if self.dying:
            self.speed = 0
            self.animation_timer += 1
            if self.animation_timer % 5 == 0:
                if self.animation_index < len(self.animation_frames) - 1:
                    self.animation_index += 1
                    self.image = self.animation_frames[self.animation_index]
                    self.mask = pygame.mask.from_surface(self.image)
                else: self.kill()

    def hit(self):
        self.hp -= 1
        if self.hp <= 0 and not self.dying: self.die()

    def slow_down(self): self.slow_timer = 120

    def die(self):
        self.dying = True
        self.animation_timer = 0


class SmallEnemy(Enemy):
    def __init__(self):
        super().__init__(
            image_name="./images/images/enemy1.png", speed=random.randint(1, 2), hp=1, score=1, 
            morale_penalty=1,
            animation_frames=["./images/images/enemy1_down1.png", "./images/images/enemy1_down2.png", "./images/images/enemy1_down3.png", "./images/images/enemy1_down4.png"]
        )

class MidEnemy(Enemy):
    def __init__(self):
        super().__init__(
            image_name="./images/images/enemy2.png", speed=random.randint(1, 2), hp=8, score=8, 
            morale_penalty=5,
            animation_frames=["./images/images/enemy2_down1.png", "./images/images/enemy2_down2.png", "./images/images/enemy2_down3.png", "./images/images/enemy2_down4.png"]
        )

class BigEnemy(Enemy):
    def __init__(self):
        super().__init__(
            image_name="./images/images/enemy3_n1.png", speed=1, hp=20, score=20, 
            morale_penalty=10,
            animation_frames=["./images/images/enemy3_down1.png", "./images/images/enemy3_down2.png", "./images/images/enemy3_down3.png", "./images/images/enemy3_down4.png", "./images/images/enemy3_down5.png", "./images/images/enemy3_down6.png"]
        )