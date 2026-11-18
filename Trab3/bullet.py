import pygame
from abc import ABC, abstractmethod
from util import colored_sprite, EventHandler
import math

def rotate(pos, angle, axis=(0, 0)):
    angle = math.radians(angle)
    x, y = pos
    ax, ay = axis

    # Translate so axis is the origin
    x -= ax
    y -= ay

    # Rotate
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)

    rx = x * cos_a - y * sin_a
    ry = x * sin_a + y * cos_a

    # Translate back
    return rx + ax, ry + ay


class Bullet(ABC):
    def __init__(self, pos, angle=0, radius=8, life_time=180):
        self.pos = pygame.Vector2(pos)
        self.origin = pygame.Vector2(pos)
        self.angle = angle
        self.life_time = life_time
        self.elapsed = 0
        self.radius = radius

        # Sprite padrão amarelo/vermelho para projéteis
        self.sprite = colored_sprite((255, 255, 0), (self.radius * 2, self.radius * 2))

    def update(self, dt):
        self.elapsed += dt
        if self.life_time and self.elapsed >= self.life_time:
            self.destroy()       

        # Calcula o movimento local e aplica rotação e origem
        move_offset = self.move()
        rotated_offset = rotate(move_offset, self.angle)
        self.pos = self.origin + pygame.Vector2(rotated_offset)

    def draw(self, screen):
        # Centraliza o blit considerando o raio
        screen.blit(self.sprite, (self.pos.x - self.radius, self.pos.y - self.radius))

    @abstractmethod
    def move(self):
        pass

    def destroy(self): 
        # Notifica o EventHandler para remover o projétil da lista de objetos do jogo
        EventHandler().notify("DestroyObj", self)


class StandardBullet(Bullet):
    """Projétil linear padrão (ótimo para twin-stick shooters e shoot'em up)."""
    def __init__(self, pos, angle=0, speed=7, life_time=180):
        super().__init__(pos, angle, radius=6, life_time=life_time)
        self.speed = speed

    def move(self):
        # Move-se em linha reta para frente ao longo do tempo
        return (self.elapsed * self.speed, 0)


class sinBullet(Bullet):
    """Projétil com movimento oscilatório (trajetória em seno)."""
    def __init__(self, pos, angle=0, life_time=180):
        super().__init__(pos, angle, radius=8, life_time=life_time)

    def move(self):
        # Avança no eixo X e oscila no eixo Y
        return (self.elapsed * 4, math.sin(self.elapsed / 10) * 30)