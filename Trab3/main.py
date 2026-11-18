import pygame
import random
from player import Player
from enemy import Enemy
from bullet import sinBullet
from util import EventHandler, circle_collistiion


pygame.init()
WIDTH = 800
HEIGHT = 600
clock = pygame.time.Clock()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Survivor / Twin-Stick Shooter - Padrão State & Events")

player = Player((400, 300))
objects = [player]


def add_obj(obj):
    if obj not in objects:
        objects.append(obj)

def remove_obj(obj):
    if obj in objects:
        objects.remove(obj)


EventHandler().subscribe("SpawnObj", add_obj)
EventHandler().subscribe("DestroyObj", remove_obj)


spawn_timer = 0


running = True
while running:
    dt = 1 

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.action_1() 
            elif event.key == pygame.K_TAB:
                player.action_2() 


    spawn_timer += 1
    if spawn_timer >= 90:
        spawn_timer = 0
        side = random.choice(['top', 'bottom', 'left', 'right'])
        if side == 'top': pos = (random.randint(0, WIDTH), -20)
        elif side == 'bottom': pos = (random.randint(0, WIDTH), HEIGHT + 20)
        elif side == 'left': pos = (-20, random.randint(0, HEIGHT))
        else: pos = (WIDTH + 20, random.randint(0, HEIGHT))
        
        enemy = Enemy(pos)
        add_obj(enemy)

    for obj in list(objects):
        if isinstance(obj, Enemy):
            obj.update(dt, player.pos)
        else:
            obj.update(dt)

  
    bullets = [o for o in objects if isinstance(o, (sinBullet))]
    enemies = [o for o in objects if isinstance(o, Enemy)]

    for b in bullets:
        for e in enemies:
            if circle_collistiion(b.pos, b.radius, e.pos, e.radius):
                e.take_damage(1)
                b.destroy() 
                break

    screen.fill((30, 30, 30))

    for obj in objects:
        obj.draw(screen)

    pygame.display.flip()
    clock.tick(60)
    