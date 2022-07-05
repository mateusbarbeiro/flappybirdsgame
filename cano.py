from moeda import Moeda
from objeto import Objeto
from pygame import sprite, image, transform


class Cano(Objeto):
    def __init__(self, x, y, posicao):
        sprite.Sprite.__init__(self)
        self.image = image.load('img/pipe.png')
        self.rect = self.image.get_rect()
        self.espacamento_cano = 150
        # posição 1 é de cima, -1 é a posição de baixo
        if posicao == 1:
            self.image = transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(self.espacamento_cano / 2)]
        if posicao == -1:
            self.rect.topleft = [x, y + int(self.espacamento_cano / 2)]

    def update(self, chao_velocidade):
        self.rect.x -= chao_velocidade
        if self.rect.right < 0:
            self.kill()