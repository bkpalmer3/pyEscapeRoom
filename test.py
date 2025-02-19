import pygame
import pytmx
import sys

# Initialize Pygame
pygame.init()

# Set up a temporary display before loading the map
screen = pygame.display.set_mode((800, 600))  # Set to any size for now

# Load the TMX map
tmx_data = pytmx.load_pygame("./Graphics/tilemaps/mainRoom.tmx")

# Constants
ZOOM = 2

# Update the display size based on the map dimensions
width = tmx_data.tilewidth * tmx_data.width * ZOOM
height = tmx_data.tileheight * tmx_data.height * ZOOM
screen = pygame.display.set_mode((width, height))


# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Draw the map
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile_image = tmx_data.get_tile_image_by_gid(gid)
                if tile_image:
                    scaled_tile = pygame.transform.scale(tile_image, (tmx_data.tilewidth * ZOOM, tmx_data.tileheight * ZOOM))
                    screen.blit(scaled_tile, (x * tmx_data.tilewidth * ZOOM, y * tmx_data.tileheight * ZOOM))

    # Update the display
    pygame.display.flip()
