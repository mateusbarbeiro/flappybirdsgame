import random
import pygame
from passaro import Passaro
from botao import Botao
from cano import Cano


class Game:
    def __init__(self):
        pygame.init()

        self.clock = pygame.time.Clock()
        self.fps = 60

        self.LARGURA = 864
        self.ALTURA = 936

        self.tela = pygame.display.set_mode((self.LARGURA, self.ALTURA))
        pygame.display.set_caption('Flappy Bird')

        # define a PythonConfigurationType
        self.fonte = pygame.font.SysFont('Comic Sans', 60)

        # define cor
        self.branco = (255, 255, 255)

        # carrega imagens
        self.imagem_fundo = pygame.image.load('img/bg.png')
        self.imagem_chao = pygame.image.load('img/ground.png')
        self.imagem_botao = pygame.image.load('img/restart.png')

        # variáveis do jogo
        self.chao_rolagem = 0
        self.chao_velocidade = 4
        self.voar = False
        self.game_over = False
        self.frequencia_cano = 1500  # milisegundos
        self.ultimo_cano = pygame.time.get_ticks() - self.frequencia_cano
        self.pontuacao = 0
        self.passou_pelo_cano = False

        self.grupo_passaro = pygame.sprite.Group()
        self.grupo_cano = pygame.sprite.Group()

        self.passaro = Passaro(100, int(self.ALTURA / 2))

        self.grupo_passaro.add(self.passaro)

    def texto_pontuacao(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        self.tela.blit(img, (x, y))

    def reiniciar_jogo(self):
        self.grupo_cano.empty()
        self.passaro.rect.x = 100
        self.passaro.rect.y = int(self.ALTURA / 2)
        self.pontuacao = 0
        self.game_over = False

    def start_game(self):

        # criando instancia do botão
        botao = Botao(self.LARGURA // 2 - 50, self.ALTURA // 2 - 100, self.imagem_botao)

        run = True
        while run:
            self.clock.tick(self.fps)

            # imagem de fundo
            self.tela.blit(self.imagem_fundo, (0, 0))

            # pássaro
            self.grupo_passaro.draw(self.tela)
            self.grupo_passaro.update(self.voar, self.game_over)
            self.grupo_cano.draw(self.tela)

            # desenhando o chão
            self.tela.blit(self.imagem_chao, (self.chao_rolagem, 768))

            # verificar pontuação
            if len(self.grupo_cano) > 0:
                if self.grupo_passaro.sprites()[0].rect.left > self.grupo_cano.sprites()[0].rect.left \
                        and self.grupo_passaro.sprites()[0].rect.right > self.grupo_cano.sprites()[0].rect.right \
                        and self.passou_pelo_cano == False:
                    self.passou_pelo_cano = True
                if self.passou_pelo_cano:
                    if self.grupo_passaro.sprites()[0].rect.left > self.grupo_cano.sprites()[0].rect.right:
                        self.pontuacao += 1
                        self.passou_pelo_cano = False

            self.texto_pontuacao(str(self.pontuacao), self.fonte, self.branco, int(self.LARGURA / 2), 20)

            # verificar a colisão
            if pygame.sprite.groupcollide(self.grupo_passaro, self.grupo_cano, False,
                                          False) or self.passaro.rect.top < 0:
                self.game_over = True

            # verificar se o pássaro atingiu o solo
            if self.passaro.rect.bottom >= 768:
                self.game_over = True
                voar = False

            if not self.game_over and self.voar == True:

                # criando novos canos
                tempo_atual = pygame.time.get_ticks()
                if tempo_atual - self.ultimo_cano > self.frequencia_cano:
                    altura_cano = random.randint(-100, 100)
                    cano_baixo = Cano(self.LARGURA, int(self.ALTURA / 2) + altura_cano, -1)
                    cano_cima = Cano(self.LARGURA, int(self.ALTURA / 2) + altura_cano, 1)
                    self.grupo_cano.add(cano_baixo)
                    self.grupo_cano.add(cano_cima)
                    self.ultimo_cano = tempo_atual

                # imagem de chão
                self.chao_rolagem -= self.chao_velocidade
                if abs(self.chao_rolagem) > 35:
                    self.chao_rolagem = 0
                self.grupo_cano.update(self.chao_velocidade)

            # verifica se o jogo acaba para dar restart
            if self.game_over:
                if botao.desenho_botao(self.tela):
                    self.reiniciar_jogo()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    run = False
                if evento.type == pygame.MOUSEBUTTONDOWN and self.voar == False and self.game_over == False:
                    self.voar = True

            pygame.display.update()

        pygame.quit()
