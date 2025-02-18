'''
DISCLAMIER

This is just where I learn the code so there is more detailed notes that help me understand how to use pygame
for the actual game check out the Game.py file that has the code formated to look nicer
this code is not actually used for the game file

'''



import pygame
from sys import exit

# Pygame init intializes everything that you need to run pygame, like starting the engine of your car
pygame.init()

# Creates the display room, set the name of the game, and initializes the code
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Escape room')
clock = pygame.time.Clock()

# code for importing and image
# variable = pygame.image.load('Path to the image').covert() <- this converts image into something python can use eaiser | convert.aplha() <- This respects the alpha values
# This will always be imported as a new surface

'''
code is in the same folder with all the different folder of the things
that you need. the folders that you will need are
1. Graphics
2. Font
3. Audio
'''
# test_surface = pygame.Surface((100,200))
# test_surface.fill('Red')
# test_font = pygame.font.Font(font type, font size)
# text_surface = test_font.render(t"ext", AA (T/F), color )

# A forever loop that keep the display running.
# in this loop we, draw all our elements & update everything

player_surf = pygame.transform.scale(pygame.image.load('graphics/Droop.png').convert_alpha(), (50,50))
# Builds a Rectangle for the player surface
player_rect = player_surf.get_rect(center = (600, 300))

m_speed = 3

#Creating the background
background_surf = pygame.Surface((800,400))
# key_pressed = False



while True:
    #pygame,event.get contatins all the different kind of events that can happen with the user interaction
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # pygame.quit is the opposite to pygame.init
            pygame.quit()
            # exit ends the program
            exit()


    # This takes imputs from the arrow keys and uses them to change the position of the player rect
    # we specifically use the keys dictiory because it allows everything to be pressed and held down instead of just one time
    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        player_rect.y -= m_speed
    if keys[pygame.K_DOWN]:
        player_rect.y += m_speed
    if keys[pygame.K_RIGHT]:
        player_rect.x += m_speed
    if keys[pygame.K_LEFT]:
        player_rect.x -= m_speed


    # Inserting the backround on the screen
    screen.blit(background_surf,(0,0))
    # .blit puts the surface on the screen
    # screen.blit(test_surface,(200,100))
    screen.blit(player_surf,player_rect)


    # These statments repoistion the player from going off the left or the right
    if player_rect.right < 0:
        player_rect.left = 800
    elif player_rect.left > 800:
        player_rect.right = 0

    # These statments repoistion the player from going off the top or bottom
    if player_rect.bottom < 0:
        player_rect.top = 400
    elif player_rect.top > 400:
        player_rect.bottom = 0
    # One way you can access controller input
    # keys = pygame.key.get_pressed()
    # keys[]

     # this creates updates the display with the new items
    pygame.display.update()
    # this sets the fram rate
    clock.tick(60)