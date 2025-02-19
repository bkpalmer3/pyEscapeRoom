# imports
import pygame
import pytmx
from sys import exit

# Constants
SPEED = 3
ZOOM = 2

# Setup and display
pygame.init()
screen = pygame.display.set_mode((800, 600))  # Set to any size for now
clock = pygame.time.Clock()

# Load the TMX map
tmx_data = pytmx.load_pygame("./Graphics/tilemaps/mainRoom.tmx")

# Update the display size based on the map dimensions
width = tmx_data.tilewidth * tmx_data.width * ZOOM
height = tmx_data.tileheight * tmx_data.height * ZOOM
screen = pygame.display.set_mode((width, height))

# Surfaces and rectangles
player_surf = pygame.transform.scale(pygame.image.load('graphics/Droop.png').convert_alpha(), (50,50))
player_rect = player_surf.get_rect(center = (600, 300))

# Game loop
while True:
    # Error handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        # Wall tool for creation
        if event.type == pygame.MOUSEMOTION: print(event.pos)

    # Draw the map
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile_image = tmx_data.get_tile_image_by_gid(gid)
                if tile_image:
                    scaled_tile = pygame.transform.scale(tile_image, (tmx_data.tilewidth * ZOOM, tmx_data.tileheight * ZOOM))
                    screen.blit(scaled_tile, (x * tmx_data.tilewidth * ZOOM, y * tmx_data.tileheight * ZOOM))

    # Surfaces
    screen.blit(player_surf,player_rect)

    # Arrow key imputs
    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        player_rect.y -= SPEED 
    if keys[pygame.K_DOWN]:
        player_rect.y += SPEED
    if keys[pygame.K_RIGHT]:
        player_rect.x += SPEED
    if keys[pygame.K_LEFT]:
        player_rect.x -= SPEED

    # Screen wrapping
    # if player_rect.right < 0:
    #     player_rect.left = 800
    # elif player_rect.left > 800:
    #     player_rect.right = 0

    # if player_rect.bottom < 0:
    #     player_rect.top = 400
    # elif player_rect.top > 400:
    #     player_rect.bottom = 0

    # Display updating and frame rate
    pygame.display.update()
    clock.tick(60)