import pygame as pg
from pygame.locals import *
from sys import exit


pg.init()
altura = 600
largura = 800

branco = (250, 250, 250)

tela = pg.display.set_mode((largura, altura))
pg.display.set_caption('oooo7')


class personagem(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.movimentos = []
        for x in range(1, 3):  # 01 - 123456 - 78
            self.movimentos.append(pg.image.load(f'parado/parado{x}.png'))
        for x in range(1, 7):
            self.movimentos.append(pg.image.load(f'anda/anda{x}.png'))
        self.movimentos.append(pg.image.load('pulo/pulo.png'))
        self.movimentos.append(pg.image.load('agacha/agacha.png'))
        self.pulo = False
        self.esquerda = False
        self.atual = 0  # imagem que vai aparece na tela
        self.inicio_animacao = 0
        self.tamanho_animacao = 2
        self.local_x = 100
        self.local_y = 300
        self.image = self.movimentos[self.atual]  # image é atributa da class pygame
        self.rect = self.image.get_rect()
        self.tm_img_x = 34
        self.tm_img_y = 36
        self.rect.topleft = self.local_x, self.local_y
        self.image = pg.transform.scale(self.image, (self.tm_img_x, self.tm_img_y))

    def ficar_parado(self):
        self.tamanho_animacao = 2
        self.inicio_animacao = 0

    def andar(self):
        self.inicio_animacao = 2
        self.tamanho_animacao = 8

    def pular(self):
        self.pulo = True
        self.forsa_pulo = 1  # variavel pulo
        self.altura = 8
        self.atual = 8

    def agachamento(self):
        self.local_y = 311
        self.tm_img_x = 34
        self.tm_img_y = 25
        self.atual = 9
        self.inicio_animacao = 9
        self.tamanho_animacao = 10

    def update(self):
        if not (self.pulo):
            self.atual += 0.5
            if self.atual >= self.tamanho_animacao:
                self.atual = self.inicio_animacao
        else:
            if self.forsa_pulo < self.altura:
                self.local_y -= 3
                self.forsa_pulo += 1
            elif self.altura <= self.forsa_pulo <= self.altura + 1:
                self.forsa_pulo += 1
            else:
                self.local_y += 3
                if self.local_y == 300:
                    self.pulo = False

        self.image = self.movimentos[int(self.atual)]
        self.rect.topleft = self.local_x, self.local_y
        self.image = pg.transform.scale(self.image, (self.tm_img_x, self.tm_img_y))
        self.image = pg.transform.flip(self.image, self.esquerda, False)
        self.tm_img_y = 36
        if not (self.pulo):
            self.local_y = 300


class Bala(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.atira = False
        self.bala_lista = []
        for x in range(1, 4):
            i_bala = pg.image.load(f'bala/00{x}.png')
            self.bala_lista.append(i_bala)

        self.id_bala = 0
        self.image = self.bala_lista[self.id_bala]
        self.rect = self.image.get_rect()
        self.rect.topleft = 100, 100
        self.image = pg.transform.flip(self.image, False, False)
        self.image = pg.transform.scale(self.image, (70, 1))

    def update(self, localizacao_x, localizacao_y, esquerda):
        # tiver munição
        self.id_bala += 1
        if self.id_bala >= len(self.bala_lista):
            self.id_bala = 0

        if esquerda:
            local_x = localizacao_x - 197
        else:
            local_x = localizacao_x + 25
        local_y = localizacao_y
        self.image = self.bala_lista[self.id_bala]
        self.rect.topleft = local_x, local_y + 15
        self.image = pg.transform.scale(self.image, (200, 13))
        self.image = pg.transform.flip(self.image, esquerda, False)
        self.atira = False


todas_as_splites = pg.sprite.Group()
personagem = personagem()
todas_as_splites.add(personagem)

image_bala = pg.sprite.Group()
bala = Bala()
image_bala.add(bala)
agacha = 0

relogio = pg.time.Clock()
while True:
    relogio.tick(20)
    tela.fill(branco)
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            exit()
        if event.type == KEYDOWN:
            if pg.key.get_pressed()[K_z] and not (personagem.pulo):
                personagem.pular()

            if pg.key.get_pressed()[K_x]:
                bala.update(personagem.local_x, personagem.local_y + agacha, personagem.esquerda)
                image_bala.draw(tela)
    if bala.atira:
        x = personagem.local_x
        y = personagem.local_y
        esq = personagem.esquerda
        image_bala.draw(tela)
        bala.update(x, y, esq)

    if pg.key.get_pressed()[K_RIGHT]:
        personagem.andar()
        personagem.esquerda = False
        personagem.local_x += 2

    elif pg.key.get_pressed()[K_LEFT]:
        personagem.andar()
        personagem.esquerda = True
        personagem.local_x -= 2

    elif pg.key.get_pressed()[K_DOWN] and not (personagem.pulo):
        personagem.agachamento()
        agacha = 5

    elif not (personagem.pulo):
        personagem.ficar_parado()
        agacha = 0

    todas_as_splites.draw(tela)
    todas_as_splites.update()
    pg.display.flip()
    # original FLP




