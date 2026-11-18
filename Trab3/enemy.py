import pygame
from abc import ABC, abstractmethod
from util import colored_sprite, EventHandler

class Enemy:
    def __init__(self, pos):
        self.pos = pygame.Vector2(pos)
        self.radius = 16
        self.health = 2
        self.state = ApproachingState(self)

    def update(self, dt, target_pos):
        self.state.update(dt, target_pos)

    def draw(self, screen):
        self.state.draw(screen)

    def change_state(self, new_state_cls):
        self.state.delete()
        self.state = new_state_cls(self)

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.destroy()
        else:
            self.change_state(StunnedState)

    def destroy(self):
        EventHandler().notify("DestroyObj", self)


class EnemyState(ABC):
    def __init__(self, enemy):
        self.E = enemy

    @abstractmethod
    def update(self, dt, target_pos):
        pass

    @abstractmethod
    def draw(self, screen):
        pass

    def delete(self):
        pass


class ApproachingState(EnemyState):
    sprite = colored_sprite((200, 50, 50)) 

    def update(self, dt, target_pos):
        target = pygame.Vector2(target_pos)
        direction = target - self.E.pos
        if direction.length() > 0:
            direction = direction.normalize()
            self.E.pos += direction * 2.5 * dt 

    def draw(self, screen):
        screen.blit(self.sprite, self.E.pos)


class StunnedState(EnemyState):
    sprite = colored_sprite((255, 255, 0)) 

    def __init__(self, enemy):
        super().__init__(enemy)
        self.stun_timer = 90 

    def update(self, dt, target_pos):
        self.stun_timer -= dt
        if self.stun_timer <= 0:
            self.E.change_state(ApproachingState)

    def draw(self, screen):
        screen.blit(self.sprite, self.E.pos)