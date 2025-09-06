
import random
import pygame

# 屏幕大小
SCREEN_RECT = pygame.Rect(0, 0, 480, 700)
# 帧率
FRAME_PER_SEC = 60
# 创建敌机的定时器事件
CREATE_ENEMY_EVENT = pygame.USEREVENT
# 英雄发射子弹的定时器事件
HERO_FIRE_EVENT = pygame.USEREVENT + 1


class GameSprite(pygame.sprite.Sprite):
    """游戏精灵基类"""
    def __init__(self, image_name, speed=1):
        super().__init__()
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self):
        self.rect.y += self.speed


class Background(GameSprite):
    """游戏背景精灵"""
    def __init__(self, is_alt=False):
        super().__init__("./images/images/Background.png")
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

        # 死亡状态相关
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
        # 左右移动
        self.rect.x += self.speed
        # 边界检查
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_RECT.width:
            self.rect.right = SCREEN_RECT.width

        # 处理死亡动画
        if self.dying:
            self.speed = 0
            self.animation_timer += 1
            if self.animation_timer % 5 == 0:
                if self.animation_index < len(self.animation_frames) - 1:
                    self.animation_index += 1
                    self.image = self.animation_frames[self.animation_index]
                else:
                    self.kill()  # 动画播放完后移除精灵
                    self.game_over = True # 设置游戏结束标志

    def fire(self):
        if not self.dying:
            for i in range(3):
                bullet = Bullet()
                bullet.rect.bottom = self.rect.y - i * 20
                bullet.rect.centerx = self.rect.centerx
                self.bullets.add(bullet)

    def die(self):
        if not self.dying:
            self.dying = True
            self.animation_timer = 0


class Bullet(GameSprite):
    """子弹精灵"""
    def __init__(self):
        super().__init__("./images/images/bullet1.png", -2)

    def update(self):
        super().update()
        if self.rect.bottom < 0:
            self.kill()


class Enemy(GameSprite):
    """敌机精灵基类"""
    def __init__(self, image_name, speed, hp, score, animation_frames):
        super().__init__(image_name, speed)
        self.hp = hp
        self.score = score
        self.rect.bottom = 0
        self.rect.x = random.randint(0, SCREEN_RECT.width - self.rect.width)
        
        # 死亡状态相关
        self.dying = False
        self.animation_frames = [pygame.image.load(frame).convert_alpha() for frame in animation_frames]
        self.animation_index = 0
        self.animation_timer = 0

    def update(self):
        super().update()
        if self.rect.top > SCREEN_RECT.height:
            self.kill() # 飞出屏幕则销毁
        
        # 处理死亡动画
        if self.dying:
            self.speed = 0
            self.animation_timer += 1
            if self.animation_timer % 5 == 0:
                if self.animation_index < len(self.animation_frames) - 1:
                    self.animation_index += 1
                    self.image = self.animation_frames[self.animation_index]
                else:
                    self.kill() # 动画播放完后销毁

    def hit(self):
        """被击中"""
        self.hp -= 1
        if self.hp <= 0 and not self.dying:
            self.die()

    def die(self):
        """开始死亡动画"""
        self.dying = True
        self.animation_timer = 0


class SmallEnemy(Enemy):
    """小型敌机"""
    def __init__(self):
        super().__init__(
            image_name="./images/images/enemy1.png",
            speed=random.randint(1, 2),
            hp=1,
            score=1,
            animation_frames=[
                "./images/images/enemy1_down1.png",
                "./images/images/enemy1_down2.png",
                "./images/images/enemy1_down3.png",
                "./images/images/enemy1_down4.png"
            ]
        )


class MidEnemy(Enemy):
    """中型敌机"""
    def __init__(self):
        super().__init__(
            image_name="./images/images/enemy2.png",
            speed=random.randint(1, 2),
            hp=8,
            score=8,
            animation_frames=[
                "./images/images/enemy2_down1.png",
                "./images/images/enemy2_down2.png",
                "./images/images/enemy2_down3.png",
                "./images/images/enemy2_down4.png"
            ]
        )


class BigEnemy(Enemy):
    """大型敌机"""
    def __init__(self):
        super().__init__(
            image_name="./images/images/enemy3_n1.png",
            speed=1,
            hp=20,
            score=20,
            animation_frames=[
                "./images/images/enemy3_down1.png",
                "./images/images/enemy3_down2.png",
                "./images/images/enemy3_down3.png",
                "./images/images/enemy3_down4.png",
                "./images/images/enemy3_down5.png",
                "./images/images/enemy3_down6.png"
            ]
        )