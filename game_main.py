import pygame
from plane_sprite import *

class PlaneGame(object):
    def __init__(self):
        print("游戏初始化")
        pygame.init()
        pygame.mixer.init()
        self.load_sound()
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        self.clock = pygame.time.Clock()
        self.__create_sprites()
        self.load_music()
        pygame.time.set_timer(CREATE_ENEMY_EVENT,1000)
        pygame.time.set_timer(HERO_FIRE_EVENT,500)
        self.score = 0

    def load_music(self):
        self.start_music="./sound/start_music.mp3"
        self.game_music="./sound/game_music.mp3"
        self.end_music="./sound/end_music.mp3"

    def play_music(self, music_path, loop=-1):
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(loop)

    def stop_music(self):
        pygame.mixer.music.stop()
    def __create_sprites(self):
        bg1=Background()
        bg2=Background(True)
        bg2.rect.y=-bg2.rect.height
        self.back_group=pygame.sprite.Group(bg1,bg2)
        self.enemy_group=pygame.sprite.Group()
        self.hero=Hero()
        self.hero_group=pygame.sprite.Group(self.hero)

    def start_game(self):
        print("游戏开始...")
        self.play_music(self.start_music)
        self.show_start_screen()
        self.stop_music()
        self.play_music(self.game_music, -1)
        while True:
            self.clock.tick(FRAME_PER_SEC)
            self.__event_handler()
            self.__check_collide()
            self.__update_sprites()
            self._display_score()
            if self.hero.game_over:
                self.stop_music()
                self.play_music(self.end_music)
                self.show_end_screen()
                break
            pygame.display.update()
    def show_start_screen(self):
        self.screen.fill((0, 0, 0))
        start_font = pygame.font.Font(None, 36)
        name_text=start_font.render("PLANE GAME", True, (255, 255, 255))
        start_text = start_font.render("Press any key to start the game", True, (255, 255, 255))
        self.screen.blit(name_text, (SCREEN_RECT.centerx - name_text.get_width() // 2, SCREEN_RECT.centery - name_text.get_height()-100))
        text_rect = start_text.get_rect(center=(SCREEN_RECT.centerx, SCREEN_RECT.centery))
        self.screen.blit(start_text, text_rect)
        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    waiting = False

    def show_end_screen(self):
        end_font = pygame.font.SysFont(None, 72)
        end_text = end_font.render("GAME OVER", True, (255, 255, 255))
        replay_text = end_font.render("Press R to replay", True, (255, 255, 255))
        quit_text = end_font.render("Press Q to quit", True, (255, 255, 255))
        score_text = end_font.render(f"Final Score: {self.score}", True, (255, 255, 255))
        self.screen.fill((0, 0, 0))
        self.screen.blit(end_text, (SCREEN_RECT.centerx - end_text.get_width() // 2, SCREEN_RECT.centery - end_text.get_height() -150))
        self.screen.blit(replay_text, (SCREEN_RECT.centerx - replay_text.get_width() // 2, SCREEN_RECT.height // 2-100))
        self.screen.blit(quit_text, (SCREEN_RECT.centerx - quit_text.get_width() // 2, SCREEN_RECT.height // 2 -50))
        self.screen.blit(score_text,(SCREEN_RECT.centerx - score_text.get_width() // 2, SCREEN_RECT.height // 2 ))
        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.restart_game()
                        waiting = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
    def restart_game(self):
        self.back_group.empty()
        self.enemy_group.empty()
        self.hero_group.empty()
        self.hero.bullets.empty()
        self.__init__()
        self.start_game()

    def __event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                PlaneGame.__game_over()
            elif event.type==CREATE_ENEMY_EVENT:
                enemy=Enemy()
                self.enemy_group.add(enemy)
            elif event.type==HERO_FIRE_EVENT:
                self.hero.fire()
        keys_pressed=pygame.key.get_pressed()
        if keys_pressed[pygame.K_RIGHT]:
            self.hero.speed=3
        elif keys_pressed[pygame.K_LEFT]:
            self.hero.speed=-3
        else:
            self.hero.speed=0

    def __check_collide(self):
        hits=pygame.sprite.groupcollide(self.hero.bullets,self.enemy_group,True,False)
        for bullet,enemies in hits.items():
            for enemy in enemies:
                if not enemy.dying:
                    enemy.die()
                    self.score+=1
                    game.explosion_sound.play()
        enemies=pygame.sprite.spritecollide(self.hero,self.enemy_group,True)
        if len(enemies)>0:
            self.hero.die()
    def __update_sprites(self):
        self.back_group.update()
        self.back_group.draw(self.screen)
        self.enemy_group.update()
        self.enemy_group.draw(self.screen)
        self.hero_group.update()
        self.hero_group.draw(self.screen)
        self.hero.bullets.update()
        self.hero.bullets.draw(self.screen)

    def _display_score(self):
        score_font = pygame.font.SysFont(None, 36)
        score_text = score_font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

    def load_sound(self):
        self.explosion_sound = pygame.mixer.Sound("./sound/explosion.mp3")

    @staticmethod
    def __game_over():
        print("游戏结束")
        pygame.quit()
        exit()



if __name__ == '__main__':
    game = PlaneGame()
    game.start_game()