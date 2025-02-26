import pygame
import pytmx

ZERO_COMPLETE = ["0 Out Of 3 Rooms Complete"]
ONE_COMPLETE = ["1 Out Of 3 Rooms Complete"]
TWO_COMPLETE = ["2 Out Of 3 Rooms Complete"]
THREE_COMPLETE = ["3 Out Of 3 Rooms Complete"]

class TileMap:
    def __init__(self, zoom, start_text):
        self.rooms = {
            "main": "./Graphics/tilemaps/mainRoom.tmx",
            "left": "./Graphics/tilemaps/leftRoom.tmx",
            "down": "./Graphics/tilemaps/bottomRoom.tmx",
            "right": "./Graphics/tilemaps/rightRoom.tmx",
            "up": "./Graphics/tilemaps/topRoom.tmx",
            "right-start": "./Graphics/tilemaps/binRoomStateStart.tmx",
            "right-1": "./Graphics/tilemaps/binRoomState13.tmx",
            "right-2": "./Graphics/tilemaps/binRoomState94.tmx",
            "right-3": "./Graphics/tilemaps/binRoomState859.tmx"
        }
        self.current_room = "main"
        self.map_data = pytmx.load_pygame(self.rooms[self.current_room])
        self.zoom = zoom

        self.current_main_text = start_text
        self.window_text = self.current_main_text

        self.binary_complete = False
        self.maze_complete = False
        self.index_complete = False

        self.index_1 = self.index_2 = self.index_3 = self.index_4 = None
        self.index_puzzle = [self.index_1, self.index_2, self.index_3, self.index_4]
        self.index_1_complete = False
        self.index_2_complete = False
        self.index_3_complete = False
        self.index_4_complete = False
        self.index_puzzle_complete = [self.index_1_complete, self.index_2_complete, self.index_3_complete, self.index_4_complete]
        self.get_index()

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

        self.buttons_pushed = ""

        self.binary_room = False
        self.correct_answer = ""
        self.user_input = ""

        
    
    def get_index(self):
        """Loads index rectangles based on the left room."""
        def load_index(layer_name):
            layer = self.map_data.get_layer_by_name(layer_name)
            if layer:
                for obj in layer:
                    return pygame.Rect(obj.x * self.zoom, obj.y * self.zoom, obj.width * self.zoom, obj.height * self.zoom)
            else:
                print(f"Warning: {layer_name} not found.")
            return None  # If no doors found
        if self.current_room == "left":
            self.index_1 = load_index("index-1")
            self.index_2 = load_index("index-2")
            self.index_3 = load_index("index-3")
            self.index_4 = load_index("index-4")
        else:
            self.index_1 = self.index_2 = self.index_3 = self.index_4 = None
            self.index_1_complete = self.index_2_complete = self.index_3_complete = self.index_4_complete = False
        
        self.index_puzzle_complete = [self.index_1_complete, self.index_2_complete, self.index_3_complete, self.index_4_complete]
        self.index_puzzle = [self.index_1, self.index_2, self.index_3, self.index_4]

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
            self.binary_room = False

            # Determine how many rooms are complete
            if self.maze_complete and self.index_complete and self.binary_complete:
                self.current_main_text = THREE_COMPLETE
            elif (self.maze_complete and self.index_complete) or (self.maze_complete and self.binary_complete) or (self.index_complete and self.binary_complete):
                self.current_main_text = TWO_COMPLETE
            elif self.maze_complete or self.index_complete or self.binary_complete:
                self.current_main_text = ONE_COMPLETE
            else:
                self.current_main_text = ZERO_COMPLETE
                
            self.computer = load_computer("Computer")
            self.window_text = self.current_main_text
        elif self.current_room == "right":
            self.binary_room = False
            self.computer = load_computer("Computer")
            self.buttons_pushed = ""
            self.window_text = ["Buttons Pushed:", "(Leave Room To Reset Numbers)", self.buttons_pushed]
        elif self.current_room == "right-start":
            self.binary_room = True
            self.computer = load_computer("Computer")
            self.correct_answer = ""
            self.window_text = ["Push The Button to Start"]
        elif self.current_room == "right-1":
            self.binary_room = True
            self.computer = load_computer("Computer")
            self.correct_answer = "13"
            self.window_text = ["What Is This Number?"]
        elif self.current_room == "right-2":
            self.binary_room = True
            self.computer = load_computer("Computer")
            self.correct_answer = "94"
            self.window_text = ["What Is This Number?"]
        elif self.current_room == "right-3":
            self.binary_room = True
            self.computer = load_computer("Computer")
            self.correct_answer = "859"
            self.window_text = ["What Is This Number?"]
        elif self.current_room == "up":
            self.binary_room = False
            self.computer = load_computer("Computer")
            self.window_text = ["0 | 0000", "1 | 0001", "2 | 0010", "3 | 0011", "4 | 0100", "5 | 0101", "6 | 0110", "7 | 0111", "8 | 1000", "9 | 1001", "A | 1010", "B | 1011", "C | 1100", "D | 1101", "E | 1110", "F | 1111"]
        elif self.current_room == "left":
            self.binary_room = False
            self.computer = load_computer("Computer")
            self.window_text = ["[1,3]", "[2,4]", "[2,6]", "[4,4]"]
        else:
            self.binary_room = False
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
        elif self.current_room == 'right-start':
            self.button_0 = load_button("Button_0")
            self.button_1 = self.button_2 = self.button_3 = self.button_4 = self.button_5 = self.button_6 = self.button_7 = self.button_8 = self.button_9 = None
        elif self.current_room == 'right-1':
            self.button_1 = load_button("Button_1")
            self.button_2 = load_button("Button_2")
            self.button_3 = load_button("Button_3")
            self.button_0 = self.button_4 = self.button_5 = self.button_6 = self.button_7 = self.button_8 = self.button_9 = None
        elif self.current_room == 'right-2':
            self.button_1 = load_button("Button_1")
            self.button_2 = load_button("Button_2")
            self.button_3 = load_button("Button_3")
            self.button_0 = self.button_4 = self.button_5 = self.button_6 = self.button_7 = self.button_8 = self.button_9 = None
        elif self.current_room == 'right-3':
            self.button_1 = load_button("Button_1")
            self.button_2 = load_button("Button_2")
            self.button_3 = load_button("Button_3")
            self.button_0 = self.button_4 = self.button_5 = self.button_6 = self.button_7 = self.button_8 = self.button_9 = None
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
        room_keys = ["up", "left", "down", "right-start", "main", "right-1", "right-2", "right-3"]  # Adjust if needed
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
            self.get_index() # Get info for idex puzzle if correct room
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
            # Create the overlay surface
            overlay_surface = pygame.Surface((overlay_width, overlay_height), pygame.SRCALPHA)
            overlay_surface.fill(overlay_color)

            # Center the overlay
            overlay_x = (screen.get_width() - overlay_width) // 2
            overlay_y = (screen.get_height() - overlay_height) // 2

            # Render the overlay on the screen
            screen.blit(overlay_surface, (overlay_x, overlay_y))

            # Render the window text
            font = pygame.font.Font(None, 24)
            line_spacing = 30  # Space between lines

            if len(self.window_text) > 10:  # Split into two columns if there's too much text
                text_x_left = overlay_x + 40
                text_x_right = overlay_x + overlay_width // 2 + 40
                text_y = overlay_y + 20

                midpoint = len(self.window_text) // 2
                left_column = self.window_text[:midpoint]
                right_column = self.window_text[midpoint:]

                # Draw left column
                self.draw_text_column(left_column, text_x_left, text_y, font, screen)
                # Draw right column
                self.draw_text_column(right_column, text_x_right, text_y, font, screen)
            else:
                text_y = overlay_y + (overlay_height - (len(self.window_text) * line_spacing)) // 2
                self.draw_text_centered(self.window_text, text_y, font, overlay_x, overlay_width, screen)

            # # Binary room input handling (if applicable)
            # if self.binary_room:
            #     self.handle_binary_input()
            #     # Draw the user's current input at the bottom of the screen
            #     self.draw_input(overlay_x, overlay_y, overlay_width, overlay_height, font, screen)

    def draw_text_column(self, text_list, x, y, font, screen):
        """Helper method to draw text in a column."""
        line_spacing = 30
        for line in text_list:
            text_surface = font.render(line, True, (255, 255, 255))
            screen.blit(text_surface, (x, y))
            y += line_spacing

    def draw_text_centered(self, text_list, y, font, overlay_x, overlay_width, screen):
        """Helper method to draw centered text."""
        line_spacing = 30
        for line in text_list:
            text_surface = font.render(line, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(overlay_x + overlay_width // 2, y))
            screen.blit(text_surface, text_rect)
            y += line_spacing

    def handle_binary_input(self):
        """Handles input for binary rooms."""
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Check answer when Enter is pressed
                    if self.user_input.lower() == self.correct_answer.lower():
                        self.handle_correct_answer()
                    self.user_input = ""  # Reset input after checking
                elif event.key == pygame.K_BACKSPACE:
                    # Remove the last character when backspace is pressed
                    self.user_input = self.user_input[:-1]
                else:
                    # Add the pressed key to the user input string
                    self.user_input += event.unicode


    def handle_correct_answer(self):
        """Handles room transition after correct answer."""
        if self.correct_answer == "13":
            self.current_room = "right-2"
        elif self.correct_answer == "94":
            self.current_room = "right-3"
        elif self.correct_answer == "859":
            self.current_room = "right-complete"

    def draw_input(self, overlay_x, overlay_y, overlay_width, overlay_height, font, screen):
        """Draws the user's input in the binary room."""
        font = pygame.font.Font(None, 24)
        line_spacing = 30  # Space between lines

        # Render the user input in the center of the screen
        answer_surface = font.render(self.user_input, True, (255, 255, 255))
        answer_rect = answer_surface.get_rect(center=(overlay_x + overlay_width // 2, (overlay_height * 2) + 10))
        screen.blit(answer_surface, answer_rect)



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

    def draw_index_puzzle(self, screen, camera_offset_x, camera_offset_y):
        """Draws door hitboxes for debugging."""
        for rect in self.index_puzzle:
            if rect:
                pygame.draw.rect(screen, (255, 255, 0), rect.move(-camera_offset_x, -camera_offset_y), 1) # Yellow outline

    def draw_computer(self, screen, camera_offset_x, camera_offset_y):
        if self.computer:
            pygame.draw.rect(screen, (255, 255, 0), self.computer.move(-camera_offset_x, -camera_offset_y), 1) # Yellow outline
