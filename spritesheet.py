import pygame

# THIS FILE IS GRABBING SINGLE FRAME FROM THE SEQUENCE DOUX.PNG

class SpriteSheet():
    def __init__(self, image):
        self.sheet = image

    def get_image(self, frame, width, height, scale, colour):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey((0, 0, 0))

        return image

    # def get_image1(self, frame, width, height, scale, colour):
    #     image = pygame.Surface((width, height)).convert_alpha()
    #     image.blit(self.sheet, (0, 0), (0, (frame * height), width, height))
    #     image = pygame.transform.scale(image, (width * scale, height * scale))
    #     image.set_colorkey((0,0,0))
    #
    #     return image