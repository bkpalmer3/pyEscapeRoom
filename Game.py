import pygame
import pytmx
import sys
from Tilemap import TileMap
from Player import Player
from Camera import Camera

# Initialize Pygame
pygame.init()

# Game window dimensions
WINDOW_WIDTH = 21 * 32
WINDOW_HEIGHT = 23 * 32
# WINDOW_WIDTH = 800
# WINDOW_HEIGHT = 600

# Set up display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Tile Map Game")

# Game settings
ZOOM = 2
SPEED = 2

# Load the tile map and player
tile_map = TileMap(ZOOM)  # Adjust the path as needed
player = Player(SPEED, ZOOM, screen, tile_map)
camera = Camera(WINDOW_WIDTH, WINDOW_HEIGHT)

# Link the player to the camera
player.set_camera(camera)

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION: print(event.pos)

    # Update game state
    player.update(tile_map.doorways, tile_map.collision_rects, tile_map)
    
    # Clear the screen
    screen.fill((0, 0, 0))
    
    # Draw the tile map and layers
    tile_map.draw_under(screen, camera.camera.x, camera.camera.y)
    player.draw(screen)  # Draw the player (with camera offset)
    tile_map.draw_over(screen, camera.camera.x, camera.camera.y)

    # Draw collision and door hitboxes for debugging (optional)
    tile_map.draw_collision(screen, camera.camera.x, camera.camera.y)
    tile_map.draw_doors(screen, camera.camera.x, camera.camera.y)

    # Update the display
    pygame.display.flip()

    # Control the frame rate (FPS)
    clock.tick(60)  # Limit to 60 frames per second

# Quit Pygame
pygame.quit()
sys.exit()
