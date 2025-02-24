import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, speed, zoom, screen, tile_map):
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
        self.window_open = False # Used to track if a window is open and if you can move

        self.animation_delay = 100
        self.last_update_time = pygame.time.get_ticks()

        self._extract_frames()
        self.image = self.sprite_frames[self.current_frame]
        self.rect = self.image.get_rect(center=(330, 330))
        self.starting_x = 336
        self.starting_y = 388
        self.rect.center = (self.starting_x, self.starting_y)
        self.camera = None  # Camera will be set externally

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

    def set_camera(self, camera):
        """Link the player to the camera."""
        self.camera = camera

    def player_controls(self, doors, collision_rects, tile_map, near_computer, events, near_button):
        keys = pygame.key.get_pressed()
        previous_action = self.current_action
        self.state = "idle"  # Default to idle unless movement is detected
        if self.window_open == False:
            if keys[pygame.K_UP]:
                self.current_action = "walk_up"
                self.rect.y -= self.speed
                if self.check_collision(collision_rects):
                    self.rect.y += self.speed
                if self.check_door(doors):
                    pass
                self.state = "moving"

            if keys[pygame.K_DOWN]:
                self.current_action = "walk_down"
                self.rect.y += self.speed
                if self.check_collision(collision_rects):
                    self.rect.y -= self.speed
                if self.check_door(doors):
                    pass
                self.state = "moving"

            if keys[pygame.K_LEFT]:
                self.current_action = "walk_left"
                self.rect.x -= self.speed
                if self.check_collision(collision_rects):
                    self.rect.x += self.speed
                if self.check_door(doors):
                    pass
                self.state = "moving"

            if keys[pygame.K_RIGHT]:
                self.current_action = "walk_right"
                self.rect.x += self.speed
                if self.check_collision(collision_rects):
                    self.rect.x -= self.speed
                if self.check_door(doors):
                    pass
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
            
            self.camera.update(self, tile_map.width, tile_map.height)

        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e and near_computer:
                tile_map.computer_display_active = not tile_map.computer_display_active
                self.window_open = not self.window_open
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e and near_button:
                tile_map.buttons_pushed += str(near_button - 1)
                tile_map.window_text = ["Buttons Pushed:", tile_map.buttons_pushed]


    def check_collision(self, collision_rects):
        for rect in collision_rects:
            if self.rect.colliderect(rect):
                return True
        return False
    
    def check_computer_collision(self, computer):
        if computer:
            if self.rect.colliderect(computer):
                return True
        return False
    
    def check_button_collision(self, buttons):
        button_num = 0
        if buttons:
            for button in buttons:
                button_num += 1
                if button and self.rect.colliderect(button):
                    return button_num
        return 0

    def check_door(self, doors):
        room_numb = 1
        for rect in doors:
            if rect and self.rect.colliderect(rect):
                return room_numb  # Return the room number instead of True
            room_numb += 1
        return None  # No door collision

    def draw(self, screen):
        # Apply camera transformations when drawing the player
        if self.camera:
            screen.blit(self.image, (self.rect.x - self.camera.camera.x, self.rect.y - self.camera.camera.y))
            pygame.draw.rect(screen, (0, 255, 0), self.rect.move(-self.camera.camera.x, -self.camera.camera.y), 1)  # Green outline for the player
        else:
            screen.blit(self.image, self.rect)

    def update(self, doors, collision_rects, tile_map, events):
        # Check if the player is near a computer
        near_computer = self.check_computer_collision(tile_map.computer)
        near_button = self.check_button_collision(tile_map.buttons)

        self.player_controls(doors, collision_rects, tile_map, near_computer, events, near_button)

        # If a door collision happens, change room
        new_room = self.check_door(doors)
        if new_room:
            tile_map.change_room(new_room, self)

        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time > self.animation_delay:
            self.current_frame = (self.current_frame + 1) % len(self.sprite_frames)
            self.image = self.sprite_frames[self.current_frame]
            self.last_update_time = current_time
