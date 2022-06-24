from objeto import Objeto
import random
import pygame

pygame.init()

clock = pygame.time.Clock()
fps = 60

LARGURA = 864
ALTURA = 936

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Flappy Bird')

# define a PythonConfigurationType
fonte = pygame.font.SysFont('Comic Sans', 60)

# define cor
branco = (255, 255, 255)

# carrega imagens
imagem_fundo = pygame.image.load('img/bg.png')
imagem_chao = pygame.image.load('img/ground.png')
imagem_botao = pygame.image.load('img/restart.png')

# variáveis do jogo
chao_rolagem = 0
chao_velocidade = 4
voar = False
game_over = False
espacamento_cano = 150
frequencia_cano = 1500  # milisegundos
ultimo_cano = pygame.time.get_ticks() - frequencia_cano
pontuacao = 0
passou_pelo_cano = False


def texto_pontuacao(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    tela.blit(img, (x, y))


def reiniciar_jogo():
    grupo_cano.empty()
    passaro.rect.x = 100
    passaro.rect.y = int(ALTURA / 2)
    pontuacao = 0
    return pontuacao

class Passaro(Objeto):
    def __init__(self, x, y):
        self.images = []
        for num in range(1, 4):
            img = pygame.image.load(f'img/bird{num}.png')
            self.images.append(img)


        pygame.sprite.Sprite.__init__(self)
        
        self.index = 0
        self.counter = 0
        
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False

    def update(self):

        if voar:
            # gravidade
            self.vel += 0.5  # sensibilidade de bater asas
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)

        if not game_over:
            # pular
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

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
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -3)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)


class Cano(Objeto):
    def __init__(self, x, y, posicao):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/pipe.png')
        self.rect = self.image.get_rect()
        # posição 1 é de cima, -1 é a posição de baixo
        if posicao == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(espacamento_cano / 2)]
        if posicao == -1:
            self.rect.topleft = [x, y + int(espacamento_cano / 2)]

    def update(self):
        self.rect.x -= chao_velocidade
        if self.rect.right < 0:
            self.kill()


class Botao:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def desenho_botao(self):

        acao = False

        # pegar posição do mouse
        posicao = pygame.mouse.get_pos()

        # verificar se mouse esta fora do Botao
        if self.rect.collidepoint(posicao):
            if pygame.mouse.get_pressed()[0] == 1:
                acao = True

        # desenho botão
        tela.blit(self.image, (self.rect.x, self.rect.y))

        return acao


grupo_passaro = pygame.sprite.Group()
grupo_cano = pygame.sprite.Group()

passaro = Passaro(100, int(ALTURA / 2))

grupo_passaro.add(passaro)

# criando instancia do botão
botao = Botao(LARGURA // 2 - 50, ALTURA // 2 - 100, imagem_botao)

run = True
while run:
    clock.tick(fps)

    # imagem de fundo
    tela.blit(imagem_fundo, (0, 0))

    # pássaro
    grupo_passaro.draw(tela)
    grupo_passaro.update()
    grupo_cano.draw(tela)

    # desenhando o chão
    tela.blit(imagem_chao, (chao_rolagem, 768))

    # verificar pontuação
    if len(grupo_cano) > 0:
        if grupo_passaro.sprites()[0].rect.left > grupo_cano.sprites()[0].rect.left \
                and grupo_passaro.sprites()[0].rect.right > grupo_cano.sprites()[0].rect.right \
                and passou_pelo_cano == False:
            passou_pelo_cano = True
        if passou_pelo_cano:
            if grupo_passaro.sprites()[0].rect.left > grupo_cano.sprites()[0].rect.right:
                pontuacao += 1
                passou_pelo_cano = False

    texto_pontuacao(str(pontuacao), fonte, branco, int(LARGURA / 2), 20)

    # verificar a colisão
    if pygame.sprite.groupcollide(grupo_passaro, grupo_cano, False, False) or passaro.rect.top < 0:
        game_over = True

    # verificar se o pássaro atingiu o solo
    if passaro.rect.bottom >= 768:
        game_over = True
        voar = False

    if not game_over and voar == True:

        # criando novos canos
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - ultimo_cano > frequencia_cano:
            altura_cano = random.randint(-100, 100)
            cano_baixo = Cano(LARGURA, int(ALTURA / 2) + altura_cano, -1)
            cano_cima = Cano(LARGURA, int(ALTURA / 2) + altura_cano, 1)
            grupo_cano.add(cano_baixo)
            grupo_cano.add(cano_cima)
            ultimo_cano = tempo_atual

        # imagem de chão
        chao_rolagem -= chao_velocidade
        if abs(chao_rolagem) > 35:
            chao_rolagem = 0
        grupo_cano.update()

    # verifica se o jogo acaba para dar restart
    if game_over:
        if botao.desenho_botao():
            game_over = False
            pontuacao = reiniciar_jogo()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            run = False
        if evento.type == pygame.MOUSEBUTTONDOWN and voar == False and game_over == False:
            voar = True

    pygame.display.update()

pygame.quit()
