import pygame

class Wall(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((1,350))
        self.rect = self.surf.get_rect(bottomright = (95,350))

    def color(self):
        self.surf.fill(255,0,0)

    def update(self):
        self.color()