import pygame


class Objeto(pygame.sprite.Sprite):
    def __init__(self, image="", vel=0, x=0, y=0, rect=""):
        self.image = image
        self.x = x
        self.y = y
        self.vel = vel
        self.rect = rect

    def renderiza(self, tela):
        tela.blit(self.image, self.rect)
