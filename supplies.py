import pygame
from base_sprites import GameSprite 

class Supply(GameSprite):
    """物资精灵基类"""
    def __init__(self, image_name, hp):
        super().__init__(image_name, 0) 
        self.hp = hp
        self.target_y = self.rect.y 

    def update(self):
        if abs(self.rect.y - self.target_y) < 2:
            self.rect.y = self.target_y
        elif self.rect.y < self.target_y:
            self.rect.y += 2
        elif self.rect.y > self.target_y:
            self.rect.y -= 2
    
    def hit(self):
        """被击中"""
        self.hp -= 1
        if self.hp <= 0:
            self.kill()

class FriendPlaneSupply(Supply):
    """友机补给"""
    def __init__(self):
        super().__init__("./images/images/life.png", hp=10)

class BulletSupply(Supply):
    """火力升级补给"""
    def __init__(self):
        super().__init__("./images/images/bullet_supply.png", hp=10)

class PiercingShotSupply(Supply):
    """穿透弹补给"""
    def __init__(self):
        super().__init__("./images/images/bomb_supply.png", hp=15) 

class SlowingShotSupply(Supply):
    """减速弹补给"""
    def __init__(self):
        super().__init__("./images/images/bomb.png", hp=15)