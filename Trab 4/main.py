#trab 4
import pygame
import random
from collision import Collider

pygame.init()

screen = pygame.display.set_mode((400, 500))
pygame.display.set_caption("Pato em Queda")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)

class Objeto:

    def __init__(self, sprite, x, y):
        self.sprite = sprite
        self.mask = pygame.mask.from_surface(sprite)
        self.x = x
        self.y = y

    def draw(self):
        screen.blit(self.sprite, (self.x, self.y))


class Pato(Objeto):

    def __init__(self, sprite, x, y):
        super().__init__(sprite, x, y)

        self.vx = 0
        self.vy = 0
        self.pontos = 0
        self.iniciado = False

    def atualizar(self):

        if self.iniciado:
            self.vy += 0.2
            self.x += self.vx
            self.y += self.vy

        if self.x < 0:
            self.x = 0
            self.vx = abs(self.vx)

        if self.x + self.sprite.get_width() > 400:
            self.x = 400 - self.sprite.get_width()
            self.vx = -abs(self.vx)



class Cursor(Objeto):
    pass


triangulo = pygame.Surface((70, 50), pygame.SRCALPHA)
pygame.draw.polygon(
    triangulo,
    (255, 80, 80),
    [(0, 50), (35, 0), (70, 50)]
)

estrela = pygame.Surface((40, 40), pygame.SRCALPHA)
pygame.draw.polygon(
    estrela,
    (255, 220, 0),
    [(20, 0), (25, 14), (40, 14),
     (28, 24), (32, 40), (20, 30),
     (8, 40), (12, 24), (0, 14), (15, 14)]
)

pato = Pato(
    pygame.image.load("base.png").convert_alpha(),
    170, 30
)

cursor = Cursor(
    pygame.image.load("cursor.png").convert_alpha(),
    170, 30
)

obstaculos = []

for i in range(8):
    x = random.randint(0, 330)
    y = random.randint(100, 430)

    obstaculos.append(
        Objeto(triangulo, x, y)
    )

bonus = []

for i in range(8):
    x = random.randint(0, 350)
    y = random.randint(100, 450)

    bonus.append(
        Objeto(estrela, x, y)
    )

collider = Collider()

tempo_movimento = 0

running = True


while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEMOTION and not pato.iniciado:
            cursor.x, cursor.y = event.pos

        if event.type == pygame.MOUSEBUTTONDOWN and not pato.iniciado:
            pato.x = cursor.x
            pato.y = cursor.y

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pato.iniciado = True
                pato.vy = 0
                pato.vx = 2

            if event.key == pygame.K_r:
                pato.x = 170
                pato.y = 30
                pato.vx = 0
                pato.vy = 0
                pato.pontos = 0
                pato.iniciado = False

   
    pato.atualizar()

    # Movimentar triângulos a cada 1 segundo
    tempo_atual = pygame.time.get_ticks()

    if tempo_atual - tempo_movimento >= 1000:

        for obstaculo in obstaculos:
            obstaculo.x = random.randint(0, 330)
            obstaculo.y = random.randint(100, 430)

        # Movimentar estrelas
        for estrela_obj in bonus:
            estrela_obj.x = random.randint(0, 350)
            estrela_obj.y = random.randint(100, 450)

        tempo_movimento = tempo_atual



    for obstaculo in obstaculos:
        if collider.colidiu(pato, obstaculo):
            collider.refletir(pato, obstaculo)
    
    for estrela_obj in bonus[:]:

        if collider.colidiu(pato, estrela_obj):

            collider.pontuar(pato, estrela_obj)

            bonus.remove(estrela_obj) 
   
    if pato.y > 500:
        pato.x = 170
        pato.y = 30
        pato.vx = 0
        pato.vy = 0
        pato.iniciado = False

    screen.fill((30, 30, 50))

    for obstaculo in obstaculos:
        obstaculo.draw()

    for estrela_obj in bonus:
        estrela_obj.draw()

    pato.draw()

    if not pato.iniciado:
        cursor.draw()

    texto = font.render(
        f"Pontos: {pato.pontos}",
        True,
        (255, 255, 255)
    )

    screen.blit(texto, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
