import pygame
import main

class Cell:
    def __init__(self, screen, color, rect_tuple, width):
        self.screen = screen
        self.color = color
        self.rect_tuple = rect_tuple
        self.width = width
        self.rect_obj = pygame.draw.rect(screen, color, rect_tuple, width)
        # self.center = self.rect_obj.center  # This is a tuple (0, 0)
        self.image = None
        self.type = None

        # if self.rect_obj.width == 150 and self.rect_obj.height == 150:
        #     IMAGE = pygame.image.load("Rasters/bulb.svg").convert_alpha()
        #     image_rect = IMAGE.get_rect()  # Get the rect of the image, which gives you its size
        #     # Calculate the position to blit the image at the center of self.rect_obj
        #     image_rect.center = self.rect_obj.center
        #     screen.blit(IMAGE, image_rect)
        #     pygame.display.flip()

        # self.index = None

    def set_image(self, image_name):
        IMAGE = pygame.image.load(str(image_name)).convert_alpha()
        image_rect = IMAGE.get_rect()
        image_rect.center = self.rect_obj.center
        self.screen.blit(IMAGE, image_rect)
        pygame.display.flip()
        self.image = IMAGE



