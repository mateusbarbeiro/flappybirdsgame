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

run = True
while run:
	clock.tick(fps)
	
	# imagem de fundo
	tela.blit(imagem_fundo, (0, 0))

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