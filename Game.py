# imports
import pygame
from sys import exit

# Setup and display
pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Escape room')
clock = pygame.time.Clock()

# Surfaces and rectangles
player_surf = pygame.transform.scale(pygame.image.load('graphics/Droop.png').convert_alpha(), (50,50))
player_rect = player_surf.get_rect(center = (600, 300))
background_surf = pygame.Surface((800,400))

# Other important variables
m_speed = 3

# Game loop
while True:
    # Error handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Surfaces
    screen.blit(background_surf,(0,0))
    screen.blit(player_surf,player_rect)

    # Arrow key imputs
    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        player_rect.y -= m_speed
    if keys[pygame.K_DOWN]:
        player_rect.y += m_speed
    if keys[pygame.K_RIGHT]:
        player_rect.x += m_speed
    if keys[pygame.K_LEFT]:
        player_rect.x -= m_speed

    # Screen wrapping
    if player_rect.right < 0:
        player_rect.left = 800
    elif player_rect.left > 800:
        player_rect.right = 0

    if player_rect.bottom < 0:
        player_rect.top = 400
    elif player_rect.top > 400:
        player_rect.bottom = 0

    # Display updating and frame rate
    pygame.display.update()
    clock.tick(60)