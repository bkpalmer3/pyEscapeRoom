import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, speed, zoom):
        super().__init__()

        self.sprite_sheets = {
            "walk_down": "./Graphics/characters/player/Seperate_Spritesheets/Walk_Down.png",
            "walk_left": "./Graphics/characters/player/Seperate_Spritesheets/Walk_Left.png",
            "walk_right": "./Graphics/characters/player/Seperate_Spritesheets/Walk_Right.png",
            "walk_up": "./Graphics/characters/player/Seperate_Spritesheets/Walk_Up.png",
            "idle_down": "./Graphics/characters/player/Seperate_Spritesheets/Idle_Down.png",
            "idle_left": "./Graphics/characters/player/Seperate_Spritesheets/Idle_Left.png",
            "idle_right": "./Graphics/characters/player/Seperate_Spritesheets/Idle_Right.png",
            "idle_up": "./Graphics/characters/player/Seperate_Spritesheets/Idle_Up.png"
        }

        self.current_action = "idle_down"  # Default starting action
        self.sprite_sheet = pygame.image.load(self.sprite_sheets[self.current_action]).convert_alpha()
        self.sprite_frames = []
        self.current_frame = 0
        self.zoom = zoom
        self.speed = speed
        self.state = "idle"  # Track whether the player is idle or moving

        self.animation_delay = 100
        self.last_update_time = pygame.time.get_ticks()

        self._extract_frames()
        self.image = self.sprite_frames[self.current_frame]
        self.rect = self.image.get_rect(center=(330, 330))
        self.starting_x = 310
        self.starting_y = 415
        self.rect.x = self.starting_x
        self.rect.y = self.starting_y

    def _extract_frames(self):
        def _get_frame(sprite_sheet, x, y, width, height, zoom):
            frame = pygame.Surface((width, height), pygame.SRCALPHA)
            frame.blit(sprite_sheet, (0, 0), pygame.Rect(x, y, width, height))
            scaled_width = int(width * zoom)
            scaled_height = int(height * zoom)
            frame = pygame.transform.scale(frame, (scaled_width, scaled_height))
            return frame

        """Extract frames from the current sprite sheet."""
        frame_width = 24
        frame_height = 24
        self.sprite_frames = []
        num_columns = self.sprite_sheet.get_width() // frame_width
        num_rows = self.sprite_sheet.get_height() // frame_height

        for row in range(num_rows):
            for col in range(num_columns):
                x = col * frame_width
                y = row * frame_height
                frame = _get_frame(self.sprite_sheet, x, y, frame_width, frame_height, self.zoom)
                self.sprite_frames.append(frame)

    def player_controls(self, collision_rects, camera_offset_x, camera_offset_y):
        keys = pygame.key.get_pressed()
        previous_action = self.current_action
        self.state = "idle"  # Default to idle unless movement is detected

        if keys[pygame.K_UP]:
            self.current_action = "walk_up"
            self.rect.y -= self.speed
            if self.check_collision(collision_rects, camera_offset_x, camera_offset_y):
                self.rect.y += self.speed
            self.state = "moving"

        if keys[pygame.K_DOWN]:
            self.current_action = "walk_down"
            self.rect.y += self.speed
            if self.check_collision(collision_rects, camera_offset_x, camera_offset_y):
                self.rect.y -= self.speed
            self.state = "moving"

        if keys[pygame.K_LEFT]:
            self.current_action = "walk_left"
            self.rect.x -= self.speed
            if self.check_collision(collision_rects, camera_offset_x, camera_offset_y):
                self.rect.x += self.speed
            self.state = "moving"

        if keys[pygame.K_RIGHT]:
            self.current_action = "walk_right"
            self.rect.x += self.speed
            if self.check_collision(collision_rects, camera_offset_x, camera_offset_y):
                self.rect.x -= self.speed
            self.state = "moving"

        # If no keys are pressed, switch to the corresponding idle animation
        if self.state == "idle":
            if "walk" in self.current_action:
                self.current_action = self.current_action.replace("walk", "idle")

        # If the action has changed, load the new sprite sheet and reset frames
        if self.current_action != previous_action:
            self.sprite_sheet = pygame.image.load(self.sprite_sheets[self.current_action]).convert_alpha()
            self._extract_frames()
            self.current_frame = 0

    def check_collision(self, collision_rects, camera_offset_x, camera_offset_y):
        for rect in collision_rects:
            if self.rect.colliderect(rect):
                return True
        return False
    def draw(self, camera_offset_x, camera_offset_y, screen):
        screen.blit(self.image, (self.rect.x - camera_offset_x, self.rect.y - camera_offset_y))
        pygame.draw.rect(screen, (0, 255, 0), self.rect.move(-camera_offset_x, -camera_offset_y), 1)  # Green outline for the player

    def update(self, collision_rects, camera_offset_x, camera_offset_y, screen):
        self.player_controls(collision_rects, camera_offset_x, camera_offset_y)

        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time > self.animation_delay:
            self.current_frame = (self.current_frame + 1) % len(self.sprite_frames)
            self.image = self.sprite_frames[self.current_frame]
            self.last_update_time = current_time
