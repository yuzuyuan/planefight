# game_main.py (AttributeError Fixed)

import pygame
import sys
import random
from plane_sprite import *


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
        
        # 初始化游戏状态
        self.state = "START"  # Possible states: START, PLAYING, GAME_OVER
        self.current_music_path = None # Add this line to track current music
        
        self.__create_sprites()
        
        # Set timer events
        pygame.time.set_timer(CREATE_ENEMY_EVENT, 1000)
        pygame.time.set_timer(HERO_FIRE_EVENT, 500)

    def __load_assets(self):
        """加载音乐和音效"""
        self.start_music = "./sound/start_music.mp3"
        self.game_music = "./sound/game_music.mp3"
        self.end_music = "./sound/end_music.mp3"
        self.explosion_sound = pygame.mixer.Sound("./sound/explosion.mp3")
        self.font = pygame.font.SysFont(None, 36)
        self.title_font = pygame.font.SysFont(None, 48)
        self.game_over_font = pygame.font.SysFont(None, 72)

    def __play_music(self, music_path, loop=-1):
        """播放背景音乐 (Corrected Method)"""
        # If the requested music is already playing, do nothing
        if self.current_music_path == music_path and pygame.mixer.music.get_busy():
            return
        
        # Load and play the new music
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(loop)
        
        # Update the currently playing music path
        self.current_music_path = music_path

    def __create_sprites(self):
        """创建精灵和精灵组"""
        bg1 = Background()
        bg2 = Background(True)
        self.back_group = pygame.sprite.Group(bg1, bg2)
        self.enemy_group = pygame.sprite.Group()
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)
        self.score = 0

    def start_game(self):
        """开始游戏主循环"""
        while True:
            self.clock.tick(FRAME_PER_SEC)
            
            if self.state == "START":
                self.__run_start_screen()
            elif self.state == "PLAYING":
                self.__run_game_logic()
            elif self.state == "GAME_OVER":
                self.__run_game_over_screen()

    def __run_start_screen(self):
        """运行开始界面逻辑"""
        self.__play_music(self.start_music)
        
        # Drawing
        self.screen.fill((0, 0, 0))
        name_text = self.title_font.render("PLANE GAME", True, (255, 255, 255))
        start_text = self.font.render("Press any key to start", True, (255, 255, 255))
        self.screen.blit(name_text, (SCREEN_RECT.centerx - name_text.get_width() // 2, SCREEN_RECT.centery - 100))
        self.screen.blit(start_text, (SCREEN_RECT.centerx - start_text.get_width() // 2, SCREEN_RECT.centery))
        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                PlaneGame.__game_over()
            if event.type == pygame.KEYDOWN:
                self.state = "PLAYING"
                self.__play_music(self.game_music)

    def __run_game_logic(self):
        """运行核心游戏逻辑"""
        self.__event_handler()
        self.__check_collide()
        self.__update_sprites()
        pygame.display.update()
        if self.hero.game_over:
            self.state = "GAME_OVER"
            self.__play_music(self.end_music)

    def __run_game_over_screen(self):
        """运行游戏结束界面逻辑"""
        # Drawing
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

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                PlaneGame.__game_over()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.__reset_game()
                    self.state = "PLAYING"
                    self.__play_music(self.game_music)
                elif event.key == pygame.K_q:
                    PlaneGame.__game_over()

    def __reset_game(self):
        """重置游戏状态"""
        print("重置游戏...")
        self.score = 0
        self.back_group.empty()
        self.enemy_group.empty()
        self.hero_group.empty()
        self.__create_sprites()

    def __event_handler(self):
        """事件监听 (只在PLAYING状态下调用)"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                PlaneGame.__game_over()
            elif event.type == CREATE_ENEMY_EVENT:
                rand_num = random.random()
                if rand_num < 0.7: self.enemy_group.add(SmallEnemy())
                elif rand_num < 0.95: self.enemy_group.add(MidEnemy())
                else: self.enemy_group.add(BigEnemy())
            elif event.type == HERO_FIRE_EVENT:
                self.hero.fire()

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_RIGHT]: self.hero.speed = 3
        elif keys_pressed[pygame.K_LEFT]: self.hero.speed = -3
        else: self.hero.speed = 0

    def __check_collide(self):
        """碰撞检测 (只在PLAYING状态下调用)"""
        hits = pygame.sprite.groupcollide(self.hero.bullets, self.enemy_group, True, False)
        for enemies in hits.values():
            for enemy in enemies:
                enemy.hit()
                if enemy.hp <= 0:
                    self.score += enemy.score
                    self.explosion_sound.play()
        
        enemies_collided = pygame.sprite.spritecollide(self.hero, self.enemy_group, True)
        if len(enemies_collided) > 0 and not self.hero.dying:
            self.hero.die()

    def __update_sprites(self):
        """更新和绘制精灵 (只在PLAYING状态下调用)"""
        self.back_group.update()
        self.back_group.draw(self.screen)
        
        self.enemy_group.update()
        self.enemy_group.draw(self.screen)
        
        self.hero_group.update()
        self.hero_group.draw(self.screen)
        
        self.hero.bullets.update()
        self.hero.bullets.draw(self.screen)

        self.__display_score()

    def __display_score(self):
        """显示分数"""
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

    @staticmethod
    def __game_over():
        """静态方法，退出游戏"""
        print("游戏结束")
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    game = PlaneGame()
    game.start_game()