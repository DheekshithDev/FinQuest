import pygame

pygame.init()

Screen_width = 500
Screen_height = 500

screen = pygame.display.set_mode((Screen_width, Screen_height))
pygame.display.set_caption('Spritesheets')
Bg = (50,50,50)
run = True
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()