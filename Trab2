from abc import ABC, abstractmethod
from collections import deque
import math
import random
import pygame


def criar_sprites_celula(tamanho):
    """
    Gera sprites (pygame.Surface) para os estados da célula.
    Caso prefira usar imagens externas, substitua cada Surface por:
    pygame.image.load("caminho/imagem.png").convert_alpha()
    """
    sprites = {}

 
    oculta = pygame.Surface((tamanho, tamanho), pygame.SRCALPHA)
    pygame.draw.rect(oculta, (72, 84, 104), (1, 1, tamanho - 2, tamanho - 2), border_radius=5)
    pygame.draw.line(oculta, (115, 130, 155), (2, 2), (tamanho - 4, 2), 2)
    pygame.draw.line(oculta, (115, 130, 155), (2, 2), (2, tamanho - 4), 2)
    pygame.draw.line(oculta, (42, 50, 64), (2, tamanho - 3), (tamanho - 3, tamanho - 3), 2)
    pygame.draw.line(oculta, (42, 50, 64), (tamanho - 3, 2), (tamanho - 3, tamanho - 3), 2)
    sprites["oculta"] = oculta

    oculta_hover = oculta.copy()
    pygame.draw.rect(oculta_hover, (255, 255, 255, 35), (1, 1, tamanho - 2, tamanho - 2), border_radius=5)
    sprites["oculta_hover"] = oculta_hover


    revelada = pygame.Surface((tamanho, tamanho), pygame.SRCALPHA)
    pygame.draw.rect(revelada, (44, 50, 62), (1, 1, tamanho - 2, tamanho - 2), border_radius=4)
    pygame.draw.rect(revelada, (58, 66, 82), (1, 1, tamanho - 2, tamanho - 2), 1, border_radius=4)
    sprites["revelada"] = revelada


    bandeiras = []
    for deslocamento in (-2, 2):
        surf = oculta.copy()
        cx, cy = tamanho // 2, tamanho // 2
      
        pygame.draw.line(surf, (230, 235, 245), (cx - 4, cy - 9), (cx - 4, cy + 9), 2)
        pygame.draw.line(surf, (230, 235, 245), (cx - 8, cy + 9), (cx + 2, cy + 9), 2)
       
        pontos = [
            (cx - 3, cy - 9),
            (cx + 9, cy - 4 + deslocamento),
            (cx - 3, cy + 1),
        ]
        pygame.draw.polygon(surf, (239, 68, 68), pontos)
        bandeiras.append(surf)
    sprites["bandeira"] = bandeiras

  
    minas = []
    for raio_faisca, cor_faisca in [(3, (250, 204, 21)), (5, (249, 115, 22))]:
        surf = revelada.copy()
        cx, cy = tamanho // 2, tamanho // 2 + 2
        raio = max(6, tamanho // 4)
        pygame.draw.circle(surf, (20, 22, 28), (cx, cy), raio)
        pygame.draw.circle(surf, (90, 98, 115), (cx - raio // 3, cy - raio // 3), max(2, raio // 4))

        pygame.draw.line(surf, (200, 200, 200), (cx + 3, cy - raio + 1), (cx + 7, cy - raio - 4), 2)
        pygame.draw.circle(surf, cor_faisca, (cx + 8, cy - raio - 5), raio_faisca)
        minas.append(surf)
    sprites["mina"] = minas

 
    explodida = pygame.Surface((tamanho, tamanho), pygame.SRCALPHA)
    pygame.draw.rect(explodida, (185, 28, 28), (1, 1, tamanho - 2, tamanho - 2), border_radius=4)
    explodida.blit(minas[1], (0, 0))
    sprites["explodida"] = explodida

    return sprites


class obj(ABC):

    def __init__(self, x, y, sprites):
        self.x = x
        self.y = y
        
        self.sprites = sprites

    def draw(self, screen):
        for s in self.sprites:
            screen.blit(s, (self.x, self.y))

    @abstractmethod
    def update(self, dt):
        pass


class Cell(obj):

    CORES_NUMEROS = {
        1: (96, 165, 250),     
        2: (74, 222, 128),    
        3: (248, 113, 113),  
        4: (192, 132, 252),   
        5: (251, 191, 36),    
        6: (45, 212, 191),   
        7: (244, 114, 182),   
        8: (203, 213, 225),   
    }

    def __init__(self, x, y, sprites, grid_pos, tamanho, fonte):
        super().__init__(x, y, [sprites["oculta"]])
        self.banco_sprites = sprites
        self.row, self.col = grid_pos
        self.tamanho = tamanho
        self.fonte = fonte

        self.tem_mina = False
        self.revelada = False
        self.bandeira = False
        self.explodida = False
        self.minas_vizinhas = 0
        self.selecionada = False

     
        self.tempo_anim = random.uniform(0.0, 1.0)
        self.escala_revelacao = 1.0
        self.atraso_animacao = 0.0

    def iniciar_animacao_revelar(self, atraso=0.0):
        self.revelada = True
        self.bandeira = False
        self.atraso_animacao = atraso
        self.escala_revelacao = 0.25

    def update(self, dt):
        self.tempo_anim += dt

        if self.revelada and self.escala_revelacao < 1.0:
            if self.atraso_animacao > 0:
                self.atraso_animacao -= dt
            else:
                self.escala_revelacao = min(1.0, self.escala_revelacao + dt * 5.5)

    def draw(self, screen):
    
        if not self.revelada:
            if self.bandeira:
                idx = int(self.tempo_anim * 4) % len(self.banco_sprites["bandeira"])
                sprite_atual = self.banco_sprites["bandeira"][idx]
            elif self.selecionada:
                sprite_atual = self.banco_sprites["oculta_hover"]
            else:
                sprite_atual = self.banco_sprites["oculta"]
        else:
            if self.explodida:
                sprite_atual = self.banco_sprites["explodida"]
            elif self.tem_mina:
                idx = int(self.tempo_anim * 5) % len(self.banco_sprites["mina"])
                sprite_atual = self.banco_sprites["mina"][idx]
            else:
                sprite_atual = self.banco_sprites["revelada"]

        if self.revelada and self.escala_revelacao < 1.0:
            novo_tam = max(4, int(self.tamanho * self.escala_revelacao))
            sprite_desenho = pygame.transform.smoothscale(sprite_atual, (novo_tam, novo_tam))
            offset = (self.tamanho - novo_tam) // 2
            screen.blit(sprite_desenho, (self.x + offset, self.y + offset))
        else:
            self.sprites = [sprite_atual]
            super().draw(screen)

            if self.revelada and not self.tem_mina and self.minas_vizinhas > 0:
                cor = self.CORES_NUMEROS.get(self.minas_vizinhas, (255, 255, 255))
                texto = self.fonte.render(str(self.minas_vizinhas), True, cor)
                rect_texto = texto.get_rect(
                    center=(self.x + self.tamanho // 2, self.y + self.tamanho // 2)
                )
                screen.blit(texto, rect_texto)

        if self.selecionada:
            pulso = int(180 + 75 * math.sin(self.tempo_anim * 6))
            pygame.draw.rect(
                screen,
                (250, 204, 21, pulso),
                (self.x + 1, self.y + 1, self.tamanho - 2, self.tamanho - 2),
                2,
                border_radius=5,
            )


class Grid(obj):

    def __init__(self, x, y, sprites, grid_size, tamanho_celula, total_minas, fonte_celula):
        super().__init__(x, y, sprites)
        self.rows, self.cols = grid_size
        self.tamanho_celula = tamanho_celula
        self.total_minas = total_minas
        self.fonte_celula = fonte_celula

        self.cursor = [0, 0]
        self.primeiro_clique = True
        self.game_over = False
        self.vitoria = False
        self.pontuacao = 0
        self.bandeiras_colocadas = 0
        self.tempo_decorrido = 0.0

        self.celulas = []
        self._construir_grade()

    def _construir_grade(self):
        self.celulas = []
        for r in range(self.rows):
            linha = []
            for c in range(self.cols):
                cx = self.x + c * self.tamanho_celula
                cy = self.y + r * self.tamanho_celula
                celula = Cell(
                    cx, cy, self.sprites, (r, c), self.tamanho_celula, self.fonte_celula
                )
                linha.append(celula)
            self.celulas.append(linha)
        self._atualizar_selecao()

    def _sortear_minas(self, seguro_r, seguro_c):
        """Distribui as minas garantindo que a primeira jogada nunca seja uma mina."""
        posicoes_validas = [
            (r, c)
            for r in range(self.rows)
            for c in range(self.cols)
            if abs(r - seguro_r) > 1 or abs(c - seguro_c) > 1
        ]
      
        if len(posicoes_validas) < self.total_minas:
            posicoes_validas = [
                (r, c)
                for r in range(self.rows)
                for c in range(self.cols)
                if (r, c) != (seguro_r, seguro_c)
            ]

        escolhidas = random.sample(posicoes_validas, min(self.total_minas, len(posicoes_validas)))
        for r, c in escolhidas:
            self.celulas[r][c].tem_mina = True

        for r in range(self.rows):
            for c in range(self.cols):
                if not self.celulas[r][c].tem_mina:
                    self.celulas[r][c].minas_vizinhas = self._contar_minas_vizinhas(r, c)

    def _contar_minas_vizinhas(self, row, col):
        total = 0
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = row + dr, col + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    if self.celulas[nr][nc].tem_mina:
                        total += 1
        return total

    def _atualizar_selecao(self):
        for r in range(self.rows):
            for c in range(self.cols):
                self.celulas[r][c].selecionada = (r == self.cursor[0] and c == self.cursor[1])

    def mover_cursor(self, d_row, d_col):
        self.cursor[0] = (self.cursor[0] + d_row) % self.rows
        self.cursor[1] = (self.cursor[1] + d_col) % self.cols
        self._atualizar_selecao()

    def selecionar_por_mouse(self, pos_mouse):
        mx, my = pos_mouse
        col = (mx - self.x) // self.tamanho_celula
        row = (my - self.y) // self.tamanho_celula
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.cursor = [row, col]
            self._atualizar_selecao()
            return (row, col)
        return None

    def alternar_bandeira(self, row=None, col=None):
        if self.game_over or self.vitoria:
            return
        if row is None or col is None:
            row, col = self.cursor

        celula = self.celulas[row][col]
        if celula.revelada:
            return

        celula.bandeira = not celula.bandeira
        self.bandeiras_colocadas += 1 if celula.bandeira else -1

    def revelar_celula(self, row=None, col=None):
        if self.game_over or self.vitoria:
            return
        if row is None or col is None:
            row, col = self.cursor

        celula = self.celulas[row][col]
        if celula.revelada or celula.bandeira:
            return

        if self.primeiro_clique:
            self._sortear_minas(row, col)
            self.primeiro_clique = False

        if celula.tem_mina:
            celula.explodida = True
            celula.iniciar_animacao_revelar(0.0)
            self.game_over = True
            self._revelar_todas_minas()
            return

        fila = deque([(row, col, 0)])
        visitados = {(row, col)}

        while fila:
            r, c, dist = fila.popleft()
            atual = self.celulas[r][c]
            if atual.bandeira:
                self.bandeiras_colocadas -= 1
            if not atual.revelada:
                atual.iniciar_animacao_revelar(atraso=dist * 0.025)
                self.pontuacao += 10 + atual.minas_vizinhas * 5

            if atual.minas_vizinhas == 0:
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < self.rows and 0 <= nc < self.cols:
                            vizinha = self.celulas[nr][nc]
                            if (nr, nc) not in visitados and not vizinha.revelada and not vizinha.tem_mina:
                                visitados.add((nr, nc))
                                fila.append((nr, nc, dist + 1))

        self._verificar_vitoria()

    def _revelar_todas_minas(self):
        for r in range(self.rows):
            for c in range(self.cols):
                cel = self.celulas[r][c]
                if cel.tem_mina and not cel.revelada:
                    cel.iniciar_animacao_revelar(atraso=random.uniform(0.05, 0.35))

    def _verificar_vitoria(self):
        for r in range(self.rows):
            for c in range(self.cols):
                cel = self.celulas[r][c]
                if not cel.tem_mina and not cel.revelada:
                    return
        self.vitoria = True
       
        self.pontuacao += max(100, 500 - int(self.tempo_decorrido) * 5)
        for r in range(self.rows):
            for c in range(self.cols):
                if self.celulas[r][c].tem_mina:
                    self.celulas[r][c].bandeira = True
        self.bandeiras_colocadas = self.total_minas

    def update(self, dt):
        if not self.primeiro_clique and not self.game_over and not self.vitoria:
            self.tempo_decorrido += dt

        for r in range(self.rows):
            for c in range(self.cols):
                self.celulas[r][c].update(dt)

    def draw(self, screen):

        largura = self.cols * self.tamanho_celula
        altura = self.rows * self.tamanho_celula
        pygame.draw.rect(
            screen,
            (22, 26, 34),
            (self.x - 8, self.y - 8, largura + 16, altura + 16),
            border_radius=10,
        )
        pygame.draw.rect(
            screen,
            (71, 85, 105),
            (self.x - 8, self.y - 8, largura + 16, altura + 16),
            2,
            border_radius=10,
        )

        for r in range(self.rows):
            for c in range(self.cols):
                self.celulas[r][c].draw(screen)
