import pygame
from base_sprites import Bullet 

class PowerUp:
    """道具效果基类"""
    display_name = "未知道具" 
    def __init__(self, owner):
        self.owner = owner 
        self.duration = 300 

    def update(self):
        self.duration -= 1
        if self.duration <= 0:
            self.owner.active_powerup = None 

    def fire(self, bullets_group):
        bullet = Bullet()
        bullet.rect.bottom = self.owner.rect.y
        bullet.rect.centerx = self.owner.rect.centerx
        bullets_group.add(bullet)

class PiercingShotPowerUp(PowerUp):
    """穿透弹道具"""
    display_name = "穿透弹"
    def __init__(self, owner):
        super().__init__(owner)
        self.shots_fired = 0

    def fire(self, bullets_group):
        self.shots_fired += 1
        if self.shots_fired % 3 == 0:
            bullet = Bullet("./images/images/bullet2.png", -5)
            bullet.is_piercing = True
        else:
            bullet = Bullet()
        
        bullet.rect.bottom = self.owner.rect.y
        bullet.rect.centerx = self.owner.rect.centerx
        bullets_group.add(bullet)

class SlowingShotPowerUp(PowerUp):
    """减速弹道具"""
    display_name = "减速弹"
    def fire(self, bullets_group):
        bullet = Bullet("./images/images/bullet1.png", -3)
        bullet.is_slowing = True
        bullet.rect.bottom = self.owner.rect.y
        bullet.rect.centerx = self.owner.rect.centerx
        bullets_group.add(bullet)