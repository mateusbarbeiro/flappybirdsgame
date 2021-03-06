from pygame import mouse, transform, sprite, image

from objeto import Objeto


class Passaro(Objeto):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = image.load(f'img/bird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False

    def aplicarGravidade(self):
        # gravidade
        self.vel += 0.5  # sensibilidade de bater asas
        if self.vel > 8:
            self.vel = 8
        if self.rect.bottom < 768:
            self.rect.y += int(self.vel)

    def detectarPulo(self):
        left, middle, right = mouse.get_pressed()
        
        if left:
            self.clicked = True
            self.vel = -5
        elif right:
            self.clicked = True
            self.vel = -10
        elif middle:
            self.clicked = True
            self.vel = +100
        else:
            self.clicked = False

    def animarPulo(self):
        # lida com a animação
        self.counter += 1
        flap_cooldown = 5

        if self.counter > flap_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
        self.image = self.images[self.index]

        # rotacionar o pássaro
        self.image = transform.rotate(self.images[self.index], self.vel * -3)

    def rotacionarPassadoMorrer(self):
        self.image = transform.rotate(self.images[self.index], -90)
