import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
fps = 60

LARGURA = 864
ALTURA = 936

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Flappy Bird')

# carrega imagens
imagem_fundo = pygame.image.load('img/bg.png')
imagem_chao = pygame.image.load('img/ground.png')

# variaveis do jogo
chao_rolagem = 0
chao_velocidade = 4

class Passaro(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.images = []
		self.index = 0
		self.counter = 0
		for num in range(1, 4):
			img = pygame.image.load(f'img/bird{num}.png')
			self.images.append(img)
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]

	def update(self):
		# lida com a animação
		self.counter += 1
		flap_cooldown = 5

		if self.counter > flap_cooldown:
			self.counter = 0
			self.index += 1
			if self.index >= len(self.images):
				self.index = 0
		self.image = self.images[self.index]

grupo_passaro = pygame.sprite.Group()
passaro = Passaro(100, int(ALTURA / 2))

grupo_passaro.add(passaro)

run = True
while run:
	clock.tick(fps)
	
	# imagem de fundo
	tela.blit(imagem_fundo, (0, 0))

	# passaro
	grupo_passaro.draw(tela)
	grupo_passaro.update()

	# imagem de chão
	tela.blit(imagem_chao, (chao_rolagem, 768))
	chao_rolagem -= chao_velocidade
	if abs(chao_rolagem) > 35:
		chao_rolagem = 0


	for evento in pygame.event.get():
		if evento.type == pygame.QUIT:
			run = False

	pygame.display.update()

pygame.quit()