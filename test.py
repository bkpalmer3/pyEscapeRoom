import pygame
import pytmx
import sys
from Tilemap import TileMap
from Player import Player

ZOOM = 2
SPEED = 2

pygame.init()
screen = pygame.display.set_mode((800, 600))  # Set to any size for now
clock = pygame.time.Clock()




# Initialize the tile map
tile_map = TileMap("./Graphics/tilemaps/mainRoom.tmx", ZOOM)
player = pygame.sprite.GroupSingle()
player.add(Player(SPEED, ZOOM))
player_sprite = player.sprite


# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Calculate camera offsets
    camera_offset_x = player_sprite.rect.x - screen.get_width() // 2
    camera_offset_y = player_sprite.rect.y - screen.get_height() // 2

    # Clamp the camera to map boundaries
    camera_offset_x = max(0, min(camera_offset_x, tile_map.width - screen.get_width()))
    camera_offset_y = max(0, min(camera_offset_y, tile_map.height - screen.get_height()))

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the map and player
    tile_map.draw_under(screen, camera_offset_x, camera_offset_y)
    player_sprite.draw(camera_offset_x, camera_offset_y, screen)
    tile_map.draw_over(screen, camera_offset_x, camera_offset_y)
    tile_map.draw_collision(screen, camera_offset_x, camera_offset_y)
    player.update(tile_map.collision_rects, camera_offset_x, camera_offset_y, screen)
    
    # Update the display
    pygame.display.update()
    clock.tick(60)
