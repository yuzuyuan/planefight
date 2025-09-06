import pygame
import sys
import random
from plane_sprite import *
from supplies import *
from powerups import *

# 物资区定义
SUPPLY_RECT = pygame.Rect(0, 0, 120, 700)
# 物资队列的垂直间距
SUPPLY_SPACING = 150
# 初始物资数量
INITIAL_SUPPLY_COUNT = 3
# 物资区整体的垂直偏移量
SUPPLY_Y_OFFSET = 50 
# 敌机密度增加事件
INCREASE_DENSITY_EVENT = pygame.USEREVENT + 3

class PlaneGame(object):
    """飞机大战主游戏"""
    def __init__(self):
        """游戏初始化"""
        print("游戏初始化")
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        self.clock = pygame.time.Clock()
        self.__load_assets()
        
        self.state = "START"
        self.current_music_path = None
        
        self.notifications = [] 
        
        self.__create_sprites()
        
        self.enemy_creation_interval = 1000 
        pygame.time.set_timer(CREATE_ENEMY_EVENT, self.enemy_creation_interval)
        
        pygame.time.set_timer(HERO_FIRE_EVENT, 500)
        pygame.time.set_timer(INCREASE_DENSITY_EVENT, 20000)

        self.level_up_timer = 0
        self.game_start_time = 0 

    def __load_assets(self):
        """加载音乐和音效"""
        self.start_music = "./sound/start_music.mp3"
        self.game_music = "./sound/game_music.mp3"
        self.end_music = "./sound/end_music.mp3"
        self.explosion_sound = pygame.mixer.Sound("./sound/explosion.mp3")
        self.font = pygame.font.SysFont(None, 36)
        self.title_font = pygame.font.SysFont(None, 48)
        self.game_over_font = pygame.font.SysFont(None, 72)
        self.level_up_font = pygame.font.SysFont(None, 48)
        self.hp_font = pygame.font.SysFont(None, 24)
        self.notification_font = pygame.font.SysFont("fangsong", 30)

    def __play_music(self, music_path, loop=-1):
        if self.current_music_path == music_path and pygame.mixer.music.get_busy():
            return
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(loop)
        self.current_music_path = music_path

    def __create_sprites(self):
        """创建精灵和精灵组"""
        bg1 = Background()
        bg2 = Background(True)
        self.back_group = pygame.sprite.Group(bg1, bg2)
        self.enemy_group = pygame.sprite.Group()
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)
        self.supply_group = pygame.sprite.Group()
        self.friend_planes_group = pygame.sprite.Group()
        self.score = 0
        self.hero.level = 1
        self.morale = 100 
        self.__init_supply_queue()

    def __init_supply_queue(self):
        """初始化物资队列"""
        self.supply_group.empty()
        supply_types = [FriendPlaneSupply, BulletSupply, PiercingShotSupply, SlowingShotSupply]
        for i in range(INITIAL_SUPPLY_COUNT):
            supply = random.choice(supply_types)()
            supply.rect.x = (SUPPLY_RECT.width - supply.rect.width) // 2
            supply.rect.y = SUPPLY_SPACING * i + SUPPLY_Y_OFFSET 
            supply.target_y = supply.rect.y
            self.supply_group.add(supply)

    def start_game(self):
        """开始游戏主循环"""
        while True:
            self.clock.tick(FRAME_PER_SEC)
            if self.state == "START": self.__run_start_screen()
            elif self.state == "PLAYING": self.__run_game_logic()
            elif self.state == "GAME_OVER": self.__run_game_over_screen()

    def __run_start_screen(self):
        self.__play_music(self.start_music)
        self.screen.fill((0, 0, 0))
        name_text = self.title_font.render("PLANE GAME", True, (255, 255, 255))
        start_text = self.font.render("Press any key to start", True, (255, 255, 255))
        self.screen.blit(name_text, (SCREEN_RECT.centerx - name_text.get_width() // 2, SCREEN_RECT.centery - 100))
        self.screen.blit(start_text, (SCREEN_RECT.centerx - start_text.get_width() // 2, SCREEN_RECT.centery))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: PlaneGame.__game_over()
            if event.type == pygame.KEYDOWN:
                self.state = "PLAYING"
                self.game_start_time = pygame.time.get_ticks() 
                self.__play_music(self.game_music)

    def __run_game_logic(self):
        self.__event_handler()
        self.__check_collide()
        self.__update_sprites()
        pygame.display.update()
        if self.hero.game_over or self.morale <= 0:
            self.state = "GAME_OVER"
            self.__play_music(self.end_music)

    def __run_game_over_screen(self):
        self.screen.fill((0, 0, 0))
        end_text = self.game_over_font.render("GAME OVER", True, (255, 0, 0))
        score_text = self.font.render(f"Final Score: {self.score}", True, (255, 255, 255))
        replay_text = self.font.render("Press 'R' to Replay", True, (255, 255, 255))
        quit_text = self.font.render("Press 'Q' to Quit", True, (255, 255, 255))
        self.screen.blit(end_text, (SCREEN_RECT.centerx - end_text.get_width() // 2, SCREEN_RECT.centery - 150))
        self.screen.blit(score_text, (SCREEN_RECT.centerx - score_text.get_width() // 2, SCREEN_RECT.centery - 50))
        self.screen.blit(replay_text, (SCREEN_RECT.centerx - replay_text.get_width() // 2, SCREEN_RECT.centery + 0))
        self.screen.blit(quit_text, (SCREEN_RECT.centerx - quit_text.get_width() // 2, SCREEN_RECT.centery + 50))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: PlaneGame.__game_over()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.__reset_game()
                    self.state = "PLAYING"
                    self.__play_music(self.game_music)
                elif event.key == pygame.K_q: PlaneGame.__game_over()

    def __reset_game(self):
        """重置游戏状态"""
        print("重置游戏...")
        self.score = 0
        self.back_group.empty()
        self.enemy_group.empty()
        self.hero_group.empty()
        self.supply_group.empty()
        self.friend_planes_group.empty()
        self.notifications = []
        self.morale = 100 
        self.game_start_time = pygame.time.get_ticks()
        self.enemy_creation_interval = 1000 
        pygame.time.set_timer(CREATE_ENEMY_EVENT, self.enemy_creation_interval)
        self.__create_sprites()

    def __event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: PlaneGame.__game_over()
            elif event.type == CREATE_ENEMY_EVENT:
                seconds_played = (pygame.time.get_ticks() - self.game_start_time) / 1000
                mid_enemy_chance = min(0.25, 0.05 + seconds_played / 240) 
                big_enemy_chance = min(0.1, 0.02 + seconds_played / 1200)
                rand_num = random.random()
                if rand_num < big_enemy_chance: self.enemy_group.add(BigEnemy())
                elif rand_num < big_enemy_chance + mid_enemy_chance: self.enemy_group.add(MidEnemy())
                else: self.enemy_group.add(SmallEnemy())
            elif event.type == INCREASE_DENSITY_EVENT:
                if self.enemy_creation_interval > 200:
                    self.enemy_creation_interval -= 100
                    pygame.time.set_timer(CREATE_ENEMY_EVENT, self.enemy_creation_interval)
                    print(f"敌机密度增加! 当前刷新间隔: {self.enemy_creation_interval}ms")
            elif event.type == HERO_FIRE_EVENT:
                self.hero.fire()
                for friend in self.friend_planes_group:
                    friend.fire(self.hero.bullets)
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_RIGHT]: self.hero.speed = 5
        elif keys_pressed[pygame.K_LEFT]: self.hero.speed = -5
        else: self.hero.speed = 0

    def __check_collide(self):
        # 子弹与敌机碰撞
        hits = pygame.sprite.groupcollide(self.hero.bullets, self.enemy_group, False, False)
        for bullet, enemies in hits.items():
            for enemy in enemies:
                enemy.hit()
                if bullet.is_slowing: enemy.slow_down()
                if not bullet.is_piercing: bullet.kill()
                if enemy.hp <= 0:
                    previous_score = self.score
                    self.score += enemy.score
                    self.explosion_sound.play()
                    if (self.score // 30) > (previous_score // 30):
                        self.hero.upgrade()
                        self.level_up_timer = 120
        
        # 英雄与敌机碰撞 (使用像素级碰撞)
        enemies_collided = pygame.sprite.spritecollide(self.hero, self.enemy_group, True, pygame.sprite.collide_mask)
        if enemies_collided and not self.hero.dying:
            self.hero.die()
        
        # 友机与敌机碰撞 (使用像素级碰撞)
        pygame.sprite.groupcollide(self.friend_planes_group, self.enemy_group, True, True, pygame.sprite.collide_mask)

        # 子弹与物资碰撞 (BUG修复逻辑)
        supply_hits = pygame.sprite.groupcollide(self.hero.bullets, self.supply_group, True, False)
        for supplies in supply_hits.values():
            for supply in supplies:
                # 在造成伤害前，先判断此物资是否为队列的第一个
                is_front_supply = False
                sorted_supplies = sorted(self.supply_group.sprites(), key=lambda s: s.rect.y)
                if sorted_supplies and supply == sorted_supplies[0]:
                    is_front_supply = True

                supply.hit() # 此方法可能会销毁（kill）物资

                if not supply.alive(): # 检查物资是否在hit后被销毁
                    self.__process_supply_reward(supply)
                    if is_front_supply:
                        self.__update_supply_queue()

    def __process_supply_reward(self, supply):
        """处理物资奖励并发送通知"""
        if isinstance(supply, FriendPlaneSupply):
            self.__add_friend_plane()
        elif isinstance(supply, BulletSupply):
            self.hero.upgrade()
            self.add_notification("主机火力升级!")
        elif isinstance(supply, PiercingShotSupply):
            self.__assign_powerup(PiercingShotPowerUp)
        elif isinstance(supply, SlowingShotSupply):
            self.__assign_powerup(SlowingShotPowerUp)
            
    def __add_friend_plane(self):
        print("获得友机！")
        if len(self.friend_planes_group) < 2: 
            new_friend = FriendPlane()
            self.friend_planes_group.add(new_friend)
            self.add_notification("获得一架僚机!")
        else:
            self.add_notification("僚机数量已达上限!")

    def __assign_powerup(self, powerup_class):
        """随机分配道具给一个单位，并创建UI通知"""
        possible_targets = [self.hero] + list(self.friend_planes_group)
        target = random.choice(possible_targets)
        target.active_powerup = powerup_class(target)
        target_name = "主机" if isinstance(target, Hero) else "僚机"
        message = f"{target_name} 获得了 [{powerup_class.display_name}]!"
        self.add_notification(message)
        print(f"道具 {powerup_class.__name__} 分配给了 {type(target).__name__}!")

    def add_notification(self, message):
        """添加一条新的UI通知"""
        self.notifications.append({"text": message, "timer": 120})

    def __update_supply_queue(self):
        """当最前面的物资被摧毁后，后面的物资向前（下）移动，并在队尾（上）补充一个新的"""
        for supply in self.supply_group:
            supply.target_y += SUPPLY_SPACING
        supply_types = [FriendPlaneSupply, BulletSupply, PiercingShotSupply, SlowingShotSupply]
        new_supply = random.choice(supply_types)()
        new_supply.rect.x = (SUPPLY_RECT.width - new_supply.rect.width) // 2
        new_supply.rect.y = SUPPLY_Y_OFFSET - SUPPLY_SPACING
        new_supply.target_y = SUPPLY_Y_OFFSET
        self.supply_group.add(new_supply)

    def __update_sprites(self):
        """更新和绘制精灵 (包含士气值检测)"""
        self.back_group.update()
        self.back_group.draw(self.screen)
        pygame.draw.rect(self.screen, (30, 30, 30), SUPPLY_RECT)
        for enemy in self.enemy_group:
            enemy.update()
            if enemy.rect.top > SCREEN_RECT.height:
                self.morale -= enemy.morale_penalty
                print(f"敌机飞过! 当前士气: {self.morale}")
                enemy.kill()
        self.enemy_group.draw(self.screen)
        self.hero_group.update()
        self.hero_group.draw(self.screen)
        self.hero.bullets.update()
        self.hero.bullets.draw(self.screen)
        self.supply_group.update()
        self.supply_group.draw(self.screen)
        for supply in self.supply_group:
            if supply.rect.bottom > 0:
                hp_text = self.hp_font.render(str(supply.hp), True, (255, 255, 255))
                text_rect = hp_text.get_rect(center=supply.rect.center)
                self.screen.blit(hp_text, text_rect)
        for i, friend in enumerate(self.friend_planes_group):
            offset = 60 * ((i // 2) + 1)
            if i % 2 == 1: offset = -offset
            friend.rect.centerx = self.hero.rect.centerx + offset
            friend.rect.bottom = self.hero.rect.bottom
        self.friend_planes_group.update()
        self.friend_planes_group.draw(self.screen)
        self.__display_ui()

    def __display_ui(self):
        """显示所有UI元素"""
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (130, 10))
        level_text = self.font.render(f"Level: {self.hero.level}", True, (255, 255, 255))
        self.screen.blit(level_text, (130, 40))
        morale_text = self.font.render(f"士气: {self.morale}", True, (255, 255, 255))
        self.screen.blit(morale_text, (SCREEN_RECT.width - morale_text.get_width() - 10, 10))
        if self.level_up_timer > 0:
            level_up_text = self.level_up_font.render("Level Up!", True, (255, 255, 0))
            text_rect = level_up_text.get_rect(center=(SCREEN_RECT.centerx, SCREEN_RECT.centery - 100))
            self.screen.blit(level_up_text, text_rect)
            self.level_up_timer -= 1
        for i in reversed(range(len(self.notifications))):
            notification = self.notifications[i]
            notification_text = self.notification_font.render(notification["text"], True, (255, 223, 0))
            y_pos = SCREEN_RECT.centery + 50 + i * 30 
            text_rect = notification_text.get_rect(center=(SCREEN_RECT.centerx, y_pos))
            self.screen.blit(notification_text, text_rect)
            notification["timer"] -= 1
            if notification["timer"] <= 0:
                self.notifications.pop(i)

    @staticmethod
    def __game_over():
        print("游戏结束")
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = PlaneGame()
    game.start_game()