import pygame
import pytmx

class TileMap:
    def __init__(self, zoom):
        self.rooms = {
            "main": "./Graphics/tilemaps/mainRoom.tmx",
            "left": "./Graphics/tilemaps/leftRoom.tmx",
            "down": "./Graphics/tilemaps/bottomRoom.tmx",
            "right": "./Graphics/tilemaps/rightRoom.tmx",
            "up": "./Graphics/tilemaps/topRoom.tmx",
        }
        self.current_room = "main"
        self.map_data = pytmx.load_pygame(self.rooms[self.current_room])
        self.zoom = zoom

        # Load collision layer
        self.collision_rects = []
        collision_layer = self.map_data.get_layer_by_name("Collision")
        if collision_layer:
            for obj in collision_layer:
                self.collision_rects.append(
                    pygame.Rect(obj.x * zoom, obj.y * zoom, obj.width * zoom, obj.height * zoom)
                )
        else:
            print("Warning: Collision layer not found.")
        
        self.computer = None
        self.get_computer()

        self.button_0 = self.button_1 = self.button_2 = self.button_3 = self.button_4 = self.button_5 = self.button_6 = self.button_7 = self.button_8 = self.button_9 = None
        self.get_buttons()
        self.buttons = [self.button_0, self.button_1, self.button_2, self.button_3, self.button_4, self.button_5, self.button_6, self.button_7, self.button_8, self.button_9]

        # Initialize doorways
        self.doorwayUp = self.doorwayLeft = self.doorwayRight = self.doorwayDown = self.doorwayOut = None
        self.get_doorways()  # Get door positions

        # Store doorways for easier iteration
        self.doorways = [self.doorwayDown, self.doorwayLeft, self.doorwayUp, self.doorwayRight, self.doorwayOut]

        # Calculate the map dimensions
        self.width = self.map_data.tilewidth * self.map_data.width * zoom
        self.height = self.map_data.tileheight * self.map_data.height * zoom

        self.computer_display_active = False

        self.window_text = ["Press E To Close"]
        self.buttons_pushed = ""

    def get_computer(self):
        """Loads the button rectangles for the room"""
        def load_computer(layer_name):
            layer = self.map_data.get_layer_by_name(layer_name)
            if layer:
                for obj in layer:
                    return pygame.Rect(obj.x * self.zoom, obj.y * self.zoom, obj.width * self.zoom, obj.height * self.zoom)
            else:
                print(f"Warning: {layer_name} not found.")
            return None  # If no doors found
        
        if self.current_room == "main":
            self.computer = load_computer("Computer")
            self.window_text = ["This Will Be Changed Later As The Way To Win"]
        elif self.current_room == "right":
            self.computer = load_computer("Computer")
            self.buttons_pushed = ""
            self.window_text = ["Buttons Pushed:", "(Leave Room To Reset Numbers)", self.buttons_pushed]
        elif self.current_room == "up":
            self.computer = load_computer("Computer")
            self.window_text = ["0 | 0000", "1 | 0001", "2 | 0010", "3 | 0011", "4 | 0100", "5 | 0101", "6 | 0110", "7 | 0111", "8 | 1000", "9 | 1001", "A | 1010", "B | 1011", "C | 1100", "D | 1101", "E | 1110", "F | 1111"]
        else:
            self.computer = None

    def get_buttons(self):
        """Loads the button rectangles for the right room"""
        def load_button(layer_name):
            layer = self.map_data.get_layer_by_name(layer_name)
            if layer:
                for obj in layer:
                    return pygame.Rect(obj.x * self.zoom, obj.y * self.zoom, obj.width * self.zoom, obj.height * self.zoom)
            else:
                print(f"Warning: {layer_name} not found.")
            return None  # If no doors found
        
        if self.current_room == 'right':
            self.button_0 = load_button("Button_0")
            self.button_1 = load_button("Button_1")
            self.button_2 = load_button("Button_2")
            self.button_3 = load_button("Button_3")
            self.button_4 = load_button("Button_4")
            self.button_5 = load_button("Button_5")
            self.button_6 = load_button("Button_6")
            self.button_7 = load_button("Button_7")
            self.button_8 = load_button("Button_8")
            self.button_9 = load_button("Button_9")
        else:
            # If it's not the correct room or if you leave the room remove the buttons
            self.button_0 = self.button_1 = self.button_2 = self.button_3 = self.button_4 = self.button_5 = self.button_6 = self.button_7 = self.button_8 = self.button_9 = None
        
        self.buttons = [self.button_0, self.button_1, self.button_2, self.button_3, self.button_4, self.button_5, self.button_6, self.button_7, self.button_8, self.button_9]

    def get_doorways(self):
        """Loads doorway rectangles based on the current room."""
        def load_door(layer_name):
            layer = self.map_data.get_layer_by_name(layer_name)
            if layer:
                for obj in layer:
                    return pygame.Rect(obj.x * self.zoom, obj.y * self.zoom, obj.width * self.zoom, obj.height * self.zoom)
            else:
                print(f"Warning: {layer_name} not found.")
            return None  # If no doors found

        if self.current_room == "main":
            # self.doorwayUp = load_door("DoorUp")
            self.doorwayRight = load_door("DoorRight")
            self.doorwayDown = load_door("DoorDown")
            self.doorwayLeft = load_door("DoorLeft")
            self.doorwayOut = None
        else:
            self.doorwayOut = load_door("Door")
            self.doorwayDown = self.doorwayLeft = self.doorwayUp = self.doorwayRight = None
        
        self.doorways = [self.doorwayDown, self.doorwayLeft, self.doorwayUp, self.doorwayRight, self.doorwayOut]

    def change_room(self, room_numb, player):
        """Updates the current room based on door index and reloads map data."""
        room_keys = ["up", "left", "down", "right", "main"]  # Adjust if needed
        if room_numb <= len(room_keys):
            self.current_room = room_keys[room_numb - 1]
            self.map_data = pytmx.load_pygame(self.rooms[self.current_room])
            self.width = self.map_data.tilewidth * self.map_data.width * self.zoom
            self.height = self.map_data.tileheight * self.map_data.height * self.zoom

            # Reload collisions and doors
            self.collision_rects = []
            collision_layer = self.map_data.get_layer_by_name("Collision")
            if collision_layer:
                for obj in collision_layer:
                    self.collision_rects.append(
                        pygame.Rect(obj.x * self.zoom, obj.y * self.zoom, obj.width * self.zoom, obj.height * self.zoom)
                    )

            self.get_doorways()  # Reload doors
            self.get_buttons() # Get Buttons if correct room
            self.get_computer() # Get the computer if there's one in the room

            # This needs to be updated
            if room_numb == 1:  # Example: entering from below
                player.rect.x = 790
                player.rect.y = 1510

            elif room_numb == 2:  # Example: entering from the left
                player.rect.x = 700
                player.rect.y = 500
                
            elif room_numb == 3:  # Example: entering from above
                player.rect.y = self.map_data.height - 10

            elif room_numb == 4:  # Example: entering from the right
                player.rect.x = 130
                player.rect.y = 500

            elif room_numb == 5:
                player.rect.x = 336
                player.rect.y = 388

            player.camera.update(player, self.width, self.height)
            player.camera.apply(player)

    def draw_layer(self, screen, camera_offset_x, camera_offset_y, layer_names):
        """Draws specified layers from the tilemap."""
        for layer in self.map_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer) and layer.name in layer_names:
                for x, y, gid in layer:
                    tile_image = self.map_data.get_tile_image_by_gid(gid)
                    if tile_image:
                        scaled_tile = pygame.transform.scale(
                            tile_image, 
                            (self.map_data.tilewidth * self.zoom, self.map_data.tileheight * self.zoom)
                        )
                        # Apply the camera offset
                        screen.blit(scaled_tile, (x * self.map_data.tilewidth * self.zoom - camera_offset_x,
                                                  y * self.map_data.tileheight * self.zoom - camera_offset_y))

    def draw_under(self, screen, camera_offset_x, camera_offset_y):
        """Draws the layers that should appear under the player (Floor, Walls)."""
        self.draw_layer(screen, camera_offset_x, camera_offset_y, {"Floor", "Walls"})

    def draw_over(self, screen, camera_offset_x, camera_offset_y):
        """Draws the layers that should appear over the player (Roof)."""
        self.draw_layer(screen, camera_offset_x, camera_offset_y, {"Roof"})

    def draw_computer_screen(self, overlay_width, overlay_height, overlay_color, screen):
        if self.computer_display_active:
            overlay_surface = pygame.Surface((overlay_width, overlay_height), pygame.SRCALPHA)  # Enable transparency
            overlay_surface.fill(overlay_color)

            overlay_x = (screen.get_width() - overlay_width) // 2  # Center X
            overlay_y = (screen.get_height() - overlay_height) // 2  # Center Y

            # Render text
            font = pygame.font.Font(None, 24)
            line_spacing = 30  # Space between lines

            if len(self.window_text) > 10:  # If there's a long list, use two columns
                text_x_left = overlay_x + 40  # Left column position
                text_x_right = overlay_x + overlay_width // 2 + 40  # Right column position
                text_y = overlay_y + 20  # Start below the top edge

                # Split text into two columns
                midpoint = len(self.window_text) // 2
                left_column = self.window_text[:midpoint]
                right_column = self.window_text[midpoint:]

                # Draw left column
                for line in left_column:
                    text_surface = font.render(line, True, (255, 255, 255))
                    screen.blit(text_surface, (text_x_left, text_y))
                    text_y += line_spacing

                # Reset Y position for right column
                text_y = overlay_y + 20

                # Draw right column
                for line in right_column:
                    text_surface = font.render(line, True, (255, 255, 255))
                    screen.blit(text_surface, (text_x_right, text_y))
                    text_y += line_spacing
            else:  # If it's just a small amount of text, center it
                text_y = overlay_y + (overlay_height - (len(self.window_text) * line_spacing)) // 2  # Center vertically
                for line in self.window_text:
                    text_surface = font.render(line, True, (255, 255, 255))
                    text_rect = text_surface.get_rect(center=(overlay_x + overlay_width // 2, text_y))
                    screen.blit(text_surface, text_rect)
                    text_y += line_spacing

            screen.blit(overlay_surface, (overlay_x, overlay_y))


    def draw_collision(self, screen, camera_offset_x, camera_offset_y):
        """Draws collision boxes (debugging only)."""
        for rect in self.collision_rects:
            pygame.draw.rect(screen, (255, 0, 0), rect.move(-camera_offset_x, -camera_offset_y), 1)  # Red outline

    def draw_doors(self, screen, camera_offset_x, camera_offset_y):
        """Draws door hitboxes for debugging."""
        for rect in self.doorways:
            if rect:
                pygame.draw.rect(screen, (0, 0, 255), rect.move(-camera_offset_x, -camera_offset_y), 1)  # Blue outline

    def draw_buttons(self, screen, camera_offset_x, camera_offset_y):
        """Draws door hitboxes for debugging."""
        for rect in self.buttons:
            if rect:
                pygame.draw.rect(screen, (255, 255, 0), rect.move(-camera_offset_x, -camera_offset_y), 1) # Yellow outline
    def draw_computer(self, screen, camera_offset_x, camera_offset_y):
        if self.computer:
            pygame.draw.rect(screen, (255, 255, 0), self.computer.move(-camera_offset_x, -camera_offset_y), 1) # Yellow outline
