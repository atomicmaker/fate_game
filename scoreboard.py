import pygame.font
from pygame.sprite import Group
from pygame import transform

from ship import Ship

class ScoreBoard:
    '''显示得分信息的类'''

    def __init__(self,ai_game):
        '''初始化显示的得分涉及的属性'''
        self.ai_game=ai_game
        self.screen=ai_game.screen
        self.screen_rect=ai_game.screen_rect
        self.settings=ai_game.settings
        self.stats=ai_game.stats

        #显示得分信息时使用的字体限制
        self.text_color=(0,255,0)
        self.font=pygame.font.SysFont(None,48)

        #准备最高得分和初始得分以及余下生命图像
        self.pre_score()
        self.pre_high_score()
        self.pre_level()
        self.pre_ship()

    def pre_score(self):
        '''将得分渲染为图像'''
        rouded_score=round(self.stats.score,-1)
        score_str='{:,}'.format(rouded_score)
        self.score_image=self.font.render(score_str,True,self.text_color)
        self.score_image_rect=self.score_image.get_rect()

        #在屏幕右上方显示图像
        self.score_image_rect.top=self.screen_rect.top
        self.score_image_rect.right=self.screen_rect.right-20

    def pre_high_score(self):
        '''将最高得分渲染成图像'''
        rounded_high_score=round(self.stats.high_score,-1)
        str_high_score='{:,}'.format(rounded_high_score)
        self.high_score_image=self.font.render(str_high_score,True,self.text_color)
        self.high_score_image_rect=self.high_score_image.get_rect()

        #在屏幕中央顶部显示
        self.high_score_image_rect.midtop=self.screen_rect.midtop

    def check_high_score(self):
        '''判断是否产生了最高分'''
        if self.stats.high_score <= self.stats.score:
            self.stats.high_score=self.stats.score
            self.pre_high_score()

    def pre_level(self):
        '''将得分渲染成图像'''
        str_level=str(self.stats.level)
        self.level_image=self.font.render(str_level,True,self.text_color)
        self.level_image_rect=self.level_image.get_rect()

        #在现在得分下方显示等级
        self.level_image_rect.midtop=self.score_image_rect.midbottom

    def pre_ship(self):
        '''显示余下生命'''
        self.ships=Group()
        for ship_number in range(self.ai_game.stats.ship_left):
            ship=Ship(self.ai_game)
            transform.scale(ship.image,(32,32))
            ship.rect.left=self.screen_rect.left + ship_number*ship.rect.width
            ship.rect.top=self.screen_rect.top
            self.ships.add(ship)

    def draw_scoreboard(self):
        '''绘制图像'''
        self.screen.blit(self.score_image,self.score_image_rect)
        self.screen.blit(self.high_score_image,self.high_score_image_rect)
        self.screen.blit(self.level_image,self.level_image_rect)
        self.ships.draw(self.screen)