from objeto import Objeto
from pygame import image, sprite, transform


class Moeda(Objeto):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = image.load('img/moeda.png')
        self.rect = self.image.get_rect()
        self.rect[0] = x
        self.rect[1] = y
        
    def update(self, chao_velocidade):
        self.rect.x -= chao_velocidade
        if self.rect.right < 0:
            self.kill()