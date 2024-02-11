import pygame
import random
import sys
import os

# # Initialize Pygame
# pygame.init()
#
# # Set up the display
# screen_width, screen_height = 800, 600
# screen = pygame.display.set_mode((screen_width, screen_height))
# pygame.display.set_caption("Dice Roller")

def roll_dice():
    # Generate a random number between 1 and 6
    dice_number = random.randint(1, 6)

    # Load the corresponding dice image
    # dice_image_path = os.path.join(os.path.dirname(__file__), f'images/dice-{dice_number}.png')

    dice_image = pygame.image.load(f'Rasters/dice_{dice_number}.jpeg')

    # Display the image
    # screen.blit(dice_image, (screen_width // 2 - dice_image.get_width() // 2, screen_height // 2 - dice_image.get_height() // 2))
    # pygame.display.flip()

    # Wait for a moment to show the image (you can adjust this time)
    # pygame.time.delay(1000)

    return dice_image, dice_number

# # Example usage
# dice_image, dice_number = roll_dice()
# print(f"Dice Number: {dice_number}")
#
# # Close the Pygame window when the user closes it
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#             pygame.quit()
#             sys.exit()
