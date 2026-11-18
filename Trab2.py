import pygame
from grid import Grid, criar_sprites_celula


pygame.init()
pygame.font.init()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Campo Minado - Grade & Puzzle")
clock = pygame.time.Clock()

font_titulo = pygame.font.Font(None, 38)
font_hud = pygame.font.Font(None, 28)
font_info = pygame.font.Font(None, 22)


def configurar_nivel(nivel, pontuacao_acumulada=0):
    """Define dimensões da grade e quantidade de minas de acordo com o nível."""
    configuracoes = [
        ((8, 10), 44, 10),   
        ((10, 12), 40, 18),  
        ((12, 15), 36, 28),  s
    ]
    if nivel <= len(configuracoes):
        grid_size, tamanho_celula, minas = configuracoes[nivel - 1]
    else:
        grid_size = (12, 16)
        tamanho_celula = 35
        minas = min(60, 28 + (nivel - 3) * 5)

    rows, cols = grid_size
    largura_grade = cols * tamanho_celula
    altura_grade = rows * tamanho_celula

    grid_x = (WIDTH - largura_grade) // 2
    grid_y = 95 + (HEIGHT - 145 - altura_grade) // 2

    sprites = criar_sprites_celula(tamanho_celula)
    font_celula = pygame.font.Font(None, int(tamanho_celula * 0.68))

    nova_grade = Grid(grid_x, grid_y, sprites, grid_size, tamanho_celula, minas, font_celula)
    nova_grade.pontuacao = pontuacao_acumulada
    return nova_grade


nivel_atual = 1
grid = configurar_nivel(nivel_atual)

objects = [grid]


def desenhar_hud(surface, grade, nivel):
   
    pygame.draw.rect(surface, (20, 24, 32), (0, 0, WIDTH, 82))
    pygame.draw.line(surface, (55, 65, 81), (0, 82), (WIDTH, 82), 2)

    titulo = font_titulo.render("CAMPO MINADO", True, (248, 250, 252))
    surface.blit(titulo, (24, 14))

    minas_restantes = grade.total_minas - grade.bandeiras_colocadas
    txt_nivel = font_hud.render(f"Nível: {nivel}", True, (96, 165, 250))
    txt_pontos = font_hud.render(f"Pontos: {grade.pontuacao}", True, (74, 222, 128))
    txt_minas = font_hud.render(f"Minas: {minas_restantes}", True, (248, 113, 113))
    txt_tempo = font_hud.render(f"Tempo: {int(grade.tempo_decorrido)}s", True, (250, 204, 21))

    surface.blit(txt_nivel, (24, 50))
    surface.blit(txt_pontos, (150, 50))
    surface.blit(txt_minas, (330, 50))
    surface.blit(txt_tempo, (480, 50))

    if grade.vitoria:
        status = font_hud.render("VITÓRIA! [N] Próx. Nível | [R] Reiniciar", True, (74, 222, 128))
        surface.blit(status, (WIDTH - status.get_width() - 20, 18))
    elif grade.game_over:
        status = font_hud.render("FIM DE JOGO! [R] ou Clique para Reiniciar", True, (248, 113, 113))
        surface.blit(status, (WIDTH - status.get_width() - 20, 18))

    rodape = font_info.render(
        "Mouse: Esq. Revelar / Dir. Bandeira   |   Teclado: Setas/WASD Mover • Espaço Revelar • F Bandeira • R Reiniciar",
        True,
        (148, 163, 184),
    )
    surface.blit(rodape, rodape.get_rect(center=(WIDTH // 2, HEIGHT - 22)))


while True:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        elif event.type == pygame.MOUSEMOTION:
            grid.selecionar_por_mouse(event.pos)

        # Uso do mouse (obrigatório)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if grid.game_over:
                grid = configurar_nivel(nivel_atual, 0)
                objects = [grid]
            elif grid.vitoria:
                nivel_atual += 1
                grid = configurar_nivel(nivel_atual, grid.pontuacao)
                objects = [grid]
            else:
                celula_clicada = grid.selecionar_por_mouse(event.pos)
                if celula_clicada is not None:
                    r, c = celula_clicada
                    if event.button == 1:  
                        grid.revelar_celula(r, c)
                    elif event.button == 3: 
                        grid.alternar_bandeira(r, c)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            elif event.key in (pygame.K_UP, pygame.K_w):
                grid.mover_cursor(-1, 0)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                grid.mover_cursor(1, 0)
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                grid.mover_cursor(0, -1)
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                grid.mover_cursor(0, 1)
            elif event.key in (pygame.K_SPACE, pygame.K_RETURN):
                grid.revelar_celula()
            elif event.key == pygame.K_f:
                grid.alternar_bandeira()
            elif event.key == pygame.K_r:
                grid = configurar_nivel(nivel_atual, 0)
                objects = [grid]
            elif event.key == pygame.K_n and grid.vitoria:
                nivel_atual += 1
                grid = configurar_nivel(nivel_atual, grid.pontuacao)
                objects = [grid]

    for item in objects:
        item.update(dt)
      
    screen.fill((30, 34, 44))
    desenhar_hud(screen, grid, nivel_atual)
