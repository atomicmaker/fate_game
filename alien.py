import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    '''表示单个外星人的类'''

    def __init__(self,ai_game):
        '''初始化外星人并设置其起始位置'''
        super().__init__()
        self.screen=ai_game.screen
        self.settings=ai_game.settings

        #加载图片并设置位置
        self.image=pygame.image.load(r'images\金闪闪.bmp')
        self.new_image=pygame.transform.scale(self.image,(100,100))
        self.rect=self.new_image.get_rect()

        self.rect.x=0
        self.rect.y=0

        self.x=float(self.rect.x)

    def check_edges(self):
        '''如果外星人位于屏幕边缘,就返回True'''
        screen_rect=self.screen.get_rect()
        if self.rect.left <= 0 or screen_rect.right <= self.rect.right:
            return True

    def update(self):
        '''向右移动外星人'''
        self.x+=(self.settings.alien_speed*
                 self.settings.fleet_direction)
        self.rect.x=self.x

    def blit_alien(self):
        '''在指定位置绘制外星人'''
        self.screen.blit(self.new_image,self.rect)
