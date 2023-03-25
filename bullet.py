import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    '''管理飞船发射的子弹'''

    def __init__(self,ai_game):
        '''在飞船当前位置创建一个子弹的类'''
        super().__init__()
        self.screen=ai_game.screen
        self.settings=ai_game.settings
        self.color=self.settings.bullet_color

        #获取子弹图像
        self.image=pygame.image.load(r'images\胜利誓约之剑.bmp')
        self.new_image=pygame.transform.scale(self.image,(20,50))#改变图片大小
        #设置子弹位置
        self.rect=self.new_image.get_rect()
        self.rect.midtop=ai_game.ship.rect.midtop

        #用小数表示子弹位置
        self.y=float(self.rect.y)
    
    def update(self):
        '''向上移动子弹'''
        #更新子弹位置
        self.y-=self.settings.bullet_speed
        #更新表示子弹的rect的位置
        self.rect.y=self.y

    def blit_bullet(self):
        '''在屏幕上绘制子弹'''
        self.screen.blit(self.new_image,self.rect)
