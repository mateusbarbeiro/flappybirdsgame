from pygame import mouse


class Botao:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def desenho_botao(self, tela):

        acao = False

        # pegar posição do mouse
        posicao = mouse.get_pos()

        # verificar se mouse esta fora do Botao
        if self.rect.collidepoint(posicao):
            if mouse.get_pressed()[0] == 1:
                acao = True

        # desenho botão
        tela.blit(self.image, (self.rect.x, self.rect.y))

        return acao
