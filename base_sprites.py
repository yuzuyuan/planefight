import pygame

class GameSprite(pygame.sprite.Sprite):
    """游戏精灵基类"""
    def __init__(self, image_name, speed=1):
        super().__init__()
        try:
            self.image = pygame.image.load(image_name)
        except pygame.error:
            print(f"警告: 无法加载图片 '{image_name}'. 将创建一个占位符.")
            self.image = pygame.Surface((40, 40))
            self.image.fill((255, 0, 255)) 
            
        self.rect = self.image.get_rect()
        self.speed = speed
        self.active_powerup = None 

    def update(self):
        self.rect.y += self.speed

class Bullet(GameSprite):
    """子弹精灵"""
    def __init__(self, image_name="./images/images/bullet1.png", speed=-3):
        super().__init__(image_name, speed)
        self.is_piercing = False
        self.is_slowing = False

    def update(self):
        super().update()
        if self.rect.bottom < 0:
            self.kill()