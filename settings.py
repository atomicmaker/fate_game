import pygame.display


class Settings:
    '''存储主程序设置类'''

    def __init__(self):
        '''初始化游戏的设置'''
        #屏幕设置
        self.screen_width=int(pygame.display.get_desktop_sizes()[0][0] *0.9)
        self.screen_hight=int(pygame.display.get_desktop_sizes()[0][1] *0.9)
        self.bg_color=(250,250,230)
        #屏幕背景
        self.back_image=pygame.image.load('images/背景.bmp')
        self.back_image=pygame.transform.scale(self.back_image,(self.screen_width,self.screen_hight))
        self.back_image_rect=self.back_image.get_rect()

        #飞船设置
        self.ship_limit=3

        #子弹设置
        self.bullet_color=(60,60,60)

        #外星人设置
        self.fleet_drop_speed=10
        #外星人移动方向
        self.fleet_direction=1

        #加快游戏节奏
        self.speedup_scale=1.2
        self.pointup_scale=1.5

    def initialize_dynamic_settings(self):
        '''初始化随游戏进行而变化的设置'''
        self.ship_speed=3.0
        self.alien_speed=2.5
        self.bullet_speed=2.5

        #外星人分数
        self.alien_point=50
    
    def increase_speed(self):
        '''提高速度设置和外星人分数'''
        self.ship_speed *=self.speedup_scale
        self.alien_speed *=self.speedup_scale
        self.bullet_speed *=self.speedup_scale
        self.alien_point=int(self.alien_point * self.pointup_scale)
        

        

