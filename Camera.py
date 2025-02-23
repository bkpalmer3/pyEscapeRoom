import pygame

class Camera:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.camera = pygame.Rect(0, 0, self.width, self.height)
        self.world_size = (width, height)

    def apply(self, entity):
        """Applies the camera offset to an entity (like the player)."""
        # Adjust the entity's rect to account for the camera's position
        return entity.rect.move(self.camera.topleft)

    def update(self, target, world_width, world_height):
        """Update the camera's position to follow the player."""
        # Calculate the camera's desired position
        x = target.rect.x - self.camera.width // 2
        y = target.rect.y - self.camera.height // 2

        # Clamp the camera's position to keep it within the world bounds
        camera_offset_x = max(0, min(x, world_width - self.camera.width))
        camera_offset_y = max(0, min(y, world_height - self.camera.height))

        # Update the camera's position
        self.camera = pygame.Rect(camera_offset_x, camera_offset_y, self.camera.width, self.camera.height)

