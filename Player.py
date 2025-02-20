import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.rotozoom(pygame.image.load('graphics/Droop.png').convert_alpha(), 0, 0.2)
        self.rect = self.image.get_rect(center = (330,330))

        self.SPEED = 3

    def player_controls(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.rect.y -= self.SPEED 
        if keys[pygame.K_DOWN]:
            self.rect.y += self.SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.SPEED
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.SPEED

    def update(self):
        self.player_controls()
    

    
