import sys
from time import sleep

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import  ScoreBoard


class AlienInvasion:
    '''管理游戏资源和行为的类'''
    def __init__(self):
        '''初始化游戏并创建游戏资源'''
        pygame.init()

        self.settings=Settings()
        self.screen=pygame.display.set_mode(
            (self.settings.screen_width,self.settings.screen_hight),pygame.RESIZABLE)
        self.screen_rect=self.screen.get_rect()

        self.stats=GameStats(self)
        
        self.ship=Ship(self)
        self.bullets=pygame.sprite.Group()
        self.aliens=pygame.sprite.Group()
        self.play_button=Button(self,'开始游戏')
        self.scoreboard=ScoreBoard(self)

        self._create_fleet()

        #设置标题
        pygame.display.set_caption('你好世界')
        #设置小图标
        pygame.display.set_icon(self.ship.image_new)
        #设置背景
        self.settings.back_image_rect.center=self.screen_rect.center

    def _check_keydown_events(self,event):
        '''响应按键'''
        if event.key==pygame.K_d or event.key==pygame.K_RIGHT:
            self.ship.moving_right=True
        elif event.key==pygame.K_a or event.key==pygame.K_LEFT:
            self.ship.moving_left=True
        elif event.key==pygame.K_SPACE:
            self._fire_bullet()

        #按Esc键结束游戏
        elif event.key==pygame.K_ESCAPE:
            sys.exit()

    def _check_keyup_events(self,event):
        '''响应松键'''
        if event.key==pygame.K_d or event.key==pygame.K_RIGHT:
            self.ship.moving_right=False
        if event.key==pygame.K_a or event.key==pygame.K_LEFT:
            self.ship.moving_left=False

    def _check_events(self):
        '''响应按键和鼠标事件'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            
            elif event.type==pygame.KEYDOWN:
               self._check_keydown_events(event)
            elif event.type==pygame.KEYUP:
                self._check_keyup_events(event)

            if event.type==pygame.MOUSEBUTTONDOWN:
                mouse_pos=pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self,mouse_pos):
        '''在玩家单击按钮时开始新游戏'''
        button_clicked=self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:  
            #重置游戏设置
            self.settings.initialize_dynamic_settings()
            
            #重置统计信息
            self.stats.reset_stats()
            self.stats.game_active=True
            self.scoreboard.pre_score()
            self.scoreboard.pre_level()
            self.scoreboard.pre_ship()

            #清空余下的外星人和子弹
            self.bullets.empty()
            self.aliens.empty()

            #创建一群新的外星人并使飞船居中
            self._create_fleet()
            self.ship.center_ship()

            #隐藏光标
            pygame.mouse.set_visible(False)
            

    def _ship_hit(self):
        '''响应飞船被外星人撞到'''
        if self.stats.ship_left >0:
            #将ship_left减1
            self.stats.ship_left-=1
            self.scoreboard.pre_ship()

            #清空余下的子弹和外星人
            self.aliens.empty()
            self.bullets.empty()

            #创建一群新的外星人，并将飞船放到屏幕底部中央
            self._create_fleet()
            self.ship.center_ship()

            #暂停0.5秒
            sleep(0.5)
        if self.stats.ship_left ==0:
            self.stats.game_active=False
            pygame.mouse.set_visible(True)
    
    def _fire_bullet(self):
        '''创建新子弹并加入编组bullets中'''
        new_bullet=Bullet(self)
        self.bullets.add(new_bullet)

    def _create_alien(self,alien_number,row_number):
        '''创建一个外星人并加入当前行'''
        alien=Alien(self)
        alien_width,alien_height=alien.rect.size
        alien.x=alien_width + 2*alien_width*alien_number
        alien.rect.x=alien.x
        alien.rect.y=alien_height + 2*alien_height * row_number
        self.aliens.add(alien)
            
    def _create_fleet(self):
        '''创建外星人群'''
        #创建一行外星人并计算一行可容纳多少外星人
        #外星人的间距为外星人的宽度       
        alien=Alien(self)
        alien_width,alien_height=alien.rect.size
        available_space_x=self.settings.screen_width-(2*alien_width)
        number_alien_x=available_space_x//(2*alien_width)

        #计算屏幕可容纳多少行外星人
        ship_height=self.ship.rect.height
        available_space_y=(self.settings.screen_hight -
                                (3*alien_height) - ship_height)
        number_rows=available_space_y//(2*alien_height)

        #创建第一行外星人
        for row_number in range(number_rows):
            for alien_number in range(number_alien_x):
                self._create_alien(alien_number,row_number)
    
    def _check_fleet_edges(self):
        '''有外星人到达边缘时采取的操作'''
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y+=self.settings.fleet_drop_speed
        self.settings.fleet_direction *=-1

    def _check_alien_bottom(self):
        '''检查是否有外星人到达屏幕底端'''
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.screen_rect.bottom:
                #像飞船被撞一样处理
                self._ship_hit()
                break
              
    def _update_screen(self):
        '''更新屏幕上的图像，并切换到新屏幕'''
        #self.screen.fill(self.settings.bg_color)
        self.screen.blit(self.settings.back_image,self.settings.back_image_rect)
        self.ship.blitme()
        self.scoreboard.draw_scoreboard()
        
        for bullet in self.bullets.sprites():
            bullet.blit_bullet()

        for alien in self.aliens.sprites():
            alien.blit_alien()

        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()

    def _update_bullet(self):
        '''更新子弹的位置并删除消失的子弹'''
        #更新子弹的位置        
        self.bullets.update()

        #删除消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collision()

    def _check_bullet_alien_collision(self):
        '''响应外星人和子弹的碰撞'''
        #删除发生碰撞的子弹和外星人

        collisions=pygame.sprite.groupcollide(
            self.bullets,self.aliens,True,True)

        if collisions:
            for value in collisions.values():
                self.stats.score +=self.settings.alien_point *len(value)
                self.scoreboard.pre_score()
                self.scoreboard.check_high_score()
        
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level +=1
            self.scoreboard.pre_level()

    def _update_aliens(self):
        '''更新外星人群中所有外星人的位置'''
        self._check_fleet_edges()
        self.aliens.update()

        #检测外星人与飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()

        self._check_alien_bottom()

    def run_game(self):
        '''开始游戏主循环'''
        while True:
            self._check_events()
            
            if self.stats.game_active:
                self._update_bullet()
                self.ship.update()
                self._update_aliens()
            
            self._update_screen()


if __name__=='__main__':
    '''创建游戏实例并运行'''
    ai=AlienInvasion()
    ai.run_game()