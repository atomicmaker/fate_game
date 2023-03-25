import pygame
from  pygame.sprite import Sprite

class Ship(Sprite):
    '''管理飞船的类'''

    def __init__(self,ai_game):
        '''初始化飞船并设置其初始位置'''
        super().__init__()
        self.screen=ai_game.screen
        self.settings=ai_game.settings
        self.screen_rect=ai_game.screen.get_rect()

        #加载飞船图片并获取其外接矩形
        self.image=pygame.image.load(r'images\saber.bmp')
        self.image=pygame.transform.scale(self.image,(85,85))
        self.image_new=pygame.transform.scale(self.image,(30,30))#改变图片大小
        self.rect=self.image.get_rect()

        #对于每艘新飞船，都将其放在屏幕底部中央
        self.rect.midbottom=self.screen_rect.midbottom

        #移动标志
        self.moving_right=False
        self.moving_left=False

        #在飞船的属性x中存储小数值
        self.x=float(self.rect.x)


    def blitme(self):
        '''在指定位置绘制飞船'''
        self.screen.blit(self.image,self.rect)

    def center_ship(self):
        '''让飞船在屏幕底部中央'''
        self.rect.midbottom=self.screen_rect.midbottom

    def update(self):
        '''根据移动标志调整飞船的位置'''
        #更新飞船而不是rect对象的x值
        if self.moving_right and self.rect.right<self.screen_rect.right:
            self.x+=self.settings.ship_speed
        elif self.moving_left and self.rect.x>0:#self.rect.x默认为左上角的位置
            self.x-=self.settings.ship_speed

        #根据self.x更新self.rect.x
        self.rect.x=self.x


