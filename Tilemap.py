import pygame
import pytmx

class TileMap:
    def __init__(self, map_file, zoom):
        self.map_data = pytmx.load_pygame(map_file)
        self.zoom = zoom

        # Used to store all the collision rectangles
        self.collision_rects = []
        collision_layer = self.map_data.get_layer_by_name("Collision")
        if collision_layer:
            for obj in collision_layer:
                rect = pygame.Rect(
                    obj.x * self.zoom, 
                    obj.y * self.zoom, 
                    obj.width * self.zoom, 
                    obj.height * self.zoom
                )
                self.collision_rects.append(rect)
        else:
            print("Warning: Collision layer not found.")

        # Calculate the map dimensions
        self.width = self.map_data.tilewidth * self.map_data.width * self.zoom
        self.height = self.map_data.tileheight * self.map_data.height * self.zoom

    def draw(self, screen, camera_offset_x, camera_offset_y):
        """Draw the map with camera offset applied."""
        for layer in self.map_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile_image = self.map_data.get_tile_image_by_gid(gid)
                    if tile_image:
                        scaled_tile = pygame.transform.scale(
                            tile_image, (self.map_data.tilewidth * self.zoom, self.map_data.tileheight * self.zoom)
                        )
                        # Apply the camera offset
                        screen.blit(scaled_tile, (x * self.map_data.tilewidth * self.zoom - camera_offset_x, y * self.map_data.tileheight * self.zoom - camera_offset_y))
        # Draw collision rectangles adjusted for camera
        for rect in self.collision_rects:
            adjusted_rect = rect.move(-camera_offset_x, -camera_offset_y)
            pygame.draw.rect(screen, (255, 0, 0), adjusted_rect, 1)  # Red outline

