import random
import pygame

from passaro import Passaro
from botao import Botao
from cano import Cano
from moeda import Moeda


class Game:
    def __init__(self):
        pygame.init()

        self.clock = pygame.time.Clock()
        self.fps = 60

        self.LARGURA = 800
        self.ALTURA = 760
        # self.LARGURA = 864
        # self.ALTURA = 936

        self.tela = pygame.display.set_mode((self.LARGURA, self.ALTURA))
        pygame.display.set_caption('Flappy Bird')

        # define a PythonConfigurationType
        self.fonte = pygame.font.SysFont('Comic Sans', 60)

        # define cor
        self.branco = (255, 255, 255)

        # carrega imagens
        self.imagem_fundo = pygame.image.load('img/bg.png')
        # (864, 768)
        self.imagem_fundo = pygame.transform.scale(self.imagem_fundo, (800, 704))

        self.imagem_chao = pygame.image.load('img/ground.png')
        # (900, 168)
        self.imagem_chao = pygame.transform.scale(self.imagem_chao, (836, 104))
        self.imagem_botao = pygame.image.load('img/restart.png')
        self.imagem_botao_iniciar = pygame.image.load('img/start.png')

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
        self.grupo_moeda = pygame.sprite.Group()

        self.passaro = Passaro(self.LARGURA / 2, int(self.ALTURA / 2))

        self.grupo_passaro.add(self.passaro)

        self.recordes_file = open("recordes.txt", "r")
        self.recordes = []
        self.fonte_recordes = pygame.font.SysFont('Comic Sans', 30)
        self.ler_recordes()
        self.salvar_recorde_lista = True

        self.cor_padrao = (225, 97, 25)

    def texto(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        self.tela.blit(img, (x, y))

    def reiniciar_jogo(self):
        self.grupo_cano.empty()
        self.grupo_moeda.empty()
        self.passaro.rect.x = 100
        self.passaro.rect.y = int(self.ALTURA / 2)
        self.pontuacao = 0
        self.game_over = False
        self.salvar_recorde_lista = True

    def ler_recordes(self):
        for recorde in self.recordes_file.readlines():
            self.recordes.append(int(recorde.replace("\n", "")))

    def salvar_recordes(self):
        self.recordes.sort(reverse=True)

        self.recordes_file.close()
        self.recordes_file = open("recordes.txt", "w")

        for y in range(0, 10 if len(self.recordes) > 10 else len(self.recordes)):
            self.recordes_file.write(str(self.recordes[y]) + '\n')

        self.recordes_file.close()

    def menu(self):
        botao = Botao(self.LARGURA // 2 - 50, self.ALTURA // 4, self.imagem_botao_iniciar)

        while True:
            self.clock.tick(self.fps)
            self.tela.blit(self.imagem_fundo, (0, 0))
            self.tela.blit(self.imagem_chao, (self.chao_rolagem, 704))

            pygame.draw.rect(self.tela, self.cor_padrao, (self.LARGURA / 1.4, self.ALTURA / 3.2, 300, 400),
                             border_radius=5)
            pygame.draw.rect(self.tela, self.branco, (self.LARGURA / 1.4, self.ALTURA / 3.2, 300, 400), width=5,
                             border_radius=5)

            pygame.draw.rect(self.tela, self.cor_padrao, (self.LARGURA / 4.8, 20, 500, 100), border_radius=5)
            pygame.draw.rect(self.tela, self.branco, (self.LARGURA / 4.8, 20, 500, 100), width=5, border_radius=5)

            self.texto("Flappy Bird", self.fonte, self.branco, int(self.LARGURA / 2) - 150, 20)

            self.texto("Recordes", self.fonte_recordes, self.branco, int(self.LARGURA / 1.2) - 50, 250)

            for pos, recorde in enumerate(self.recordes):
                self.texto(f"{pos + 1}. {recorde}", self.fonte_recordes, self.branco, int(self.LARGURA / 1.15) - 50,
                           300 + (30 * pos))

            self.grupo_passaro.draw(self.tela)
            self.passaro.animarPulo()

            if botao.desenho_botao(self.tela):
                break

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.salvar_recordes()
                    pygame.quit()

            pygame.display.update()

        self.reiniciar_jogo()
        self.start_game()

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
            self.passaro.aplicarGravidade()

            if not self.game_over:
                self.passaro.detectarPulo()
                self.passaro.animarPulo()
            else:
                self.passaro.rotacionarPassadoMorrer()

            self.grupo_cano.draw(self.tela)
            self.grupo_moeda.draw(self.tela)

            # desenhando o chão
            self.tela.blit(self.imagem_chao, (self.chao_rolagem, 704))

            # verificar pontuação
            if len(self.grupo_cano) > 0:
                if self.grupo_passaro.sprites()[0].rect.left > self.grupo_cano.sprites()[0].rect.left \
                        and self.grupo_passaro.sprites()[0].rect.right > self.grupo_cano.sprites()[0].rect.right \
                        and self.passou_pelo_cano == False:
                    self.passou_pelo_cano = True
                if self.passou_pelo_cano:
                    if self.grupo_passaro.sprites()[0].rect.left > self.grupo_cano.sprites()[0].rect.right:
                        if not self.grupo_cano.sprites()[0].passou:
                            self.grupo_cano.sprites()[0].passou = True

                            self.pontuacao += 1
                            self.passou_pelo_cano = False

            self.texto(str(self.pontuacao), self.fonte, self.branco, int(self.LARGURA / 2), 20)

            # verificar a colisão
            if pygame.sprite.groupcollide(self.grupo_passaro, self.grupo_cano, False,
                                          False) or self.passaro.rect.top < 0:
                self.game_over = True

            if pygame.sprite.groupcollide(self.grupo_passaro, self.grupo_moeda, False, True):
                self.pontuacao += 5

            # verificar se o pássaro 
            # atingiu o solo
            if self.passaro.rect.bottom >= 768:
                self.game_over = True
                self.voar = False

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
                    self.grupo_moeda.add(Moeda(cano_baixo.rect[0] + cano_baixo.rect[2] + cano_baixo.espacamento_cano,
                                               random.randrange(int(self.LARGURA * 0.4), int(self.LARGURA * 0.8))))

                # imagem de chão
                self.chao_rolagem -= self.chao_velocidade
                if abs(self.chao_rolagem) > 35:
                    self.chao_rolagem = 0
                self.grupo_cano.update(self.chao_velocidade)
                self.grupo_moeda.update(self.chao_velocidade)

            # verifica se o jogo acaba para dar restart
            if self.game_over:
                if self.salvar_recorde_lista:
                    self.recordes.append(self.pontuacao)
                    self.salvar_recorde_lista = False

                if botao.desenho_botao(self.tela):
                    self.reiniciar_jogo()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    run = False
                if evento.type == pygame.MOUSEBUTTONDOWN and self.voar == False and self.game_over == False:
                    self.voar = True

            pygame.display.update()

        self.salvar_recordes()
        pygame.quit()
