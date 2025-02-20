import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.transform.rotozoom(pygame.image.load('graphics/Droop.png').convert_alpha(), 0, 0.2)
        self.rect = self.image.get_rect(center = (330,330))

        self.speed = speed

    def player_controls(self, collision_rects, camera_offset_x, camera_offset_y):
        keys = pygame.key.get_pressed()

        # Make temporary movements and check collisions
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
            if self.check_collision(collision_rects, camera_offset_x, camera_offset_y):
                self.rect.y += self.speed  # Undo movement

        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
            if self.check_collision(collision_rects, camera_offset_x, camera_offset_y):
                self.rect.y -= self.speed

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            if self.check_collision(collision_rects, camera_offset_x, camera_offset_y):
                self.rect.x += self.speed

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            if self.check_collision(collision_rects, camera_offset_x, camera_offset_y):
                self.rect.x -= self.speed

    def check_collision(self, collision_rects, camera_offset_x, camera_offset_y):
        for rect in collision_rects:
            # Adjust each collision rectangle by the camera offset
            if self.rect.colliderect(rect):
                return True
        return False


    def draw(self, camera_offset_x, camera_offset_y, screen):
        screen.blit(self.image, (self.rect.x - camera_offset_x, self.rect.y - camera_offset_y))
        pygame.draw.rect(screen, (0, 255, 0), self.rect.move(-camera_offset_x, -camera_offset_y), 1)  # Green outline for the player
        
        

    def update(self,collision_rects, camera_offset_x, camera_offset_y, screen):
        self.player_controls(collision_rects, camera_offset_x, camera_offset_y)

