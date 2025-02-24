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
