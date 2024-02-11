import pygame, sys
import colors
import main

pygame.init()

MAIN_WIDTH, MAIN_HEIGHT = 500, 700

SCREEN = pygame.display.set_mode((MAIN_WIDTH, MAIN_HEIGHT))
pygame.display.set_caption("Educative Financial Hack")
SCREEN.fill(colors.CREAM_COLOR)

IMAGE = pygame.image.load(f'Rasters/intro_page_header.png')
image_width, image_height = IMAGE.get_size()
# Calculate the position to center the image
image_x = (MAIN_WIDTH - image_width) // 2
# image_y = (MAIN_HEIGHT - image_height) // 2

SCREEN.blit(IMAGE, (image_x, 0))


pygame.display.update()

font_size = 24
font = pygame.font.Font(None, font_size)  # Default font

# Render the text # Button 1
text = "Your Current Level: BEGINNER"
text_surface = font.render(text, True, colors.BLACK)

SCREEN.blit(text_surface, (150, 220))

# Button properties
button_color = colors.WHITE
button_hover_color = colors.GRAY
font = pygame.font.Font("C:\Windows\Fonts\8514fix.fon", 30)

# 1st Button
beginner_button = pygame.Rect(200, 260, 140, 50)  # x, y, width, height
button_text = "Beginner"

# 2nd Button
inter_button = pygame.Rect(200, 360, 140, 50)  # x, y, width, height
button_text_2 = "Intermediate"

# 3rd Button
professional_button = pygame.Rect(200, 460, 140, 50)  # x, y, width, height
button_text_3 = "Professional"

# 4th Button
expert_button = pygame.Rect(200, 560, 140, 50)  # x, y, width, height
button_text_4 = "Expert"

def draw_button(surface, rect, color, text):
    pygame.draw.rect(surface, color, rect)  # Draw button
    text_surf = font.render(text, True, colors.BLACK)
    # Center text on button
    surface.blit(text_surf, text_surf.get_rect(center=rect.center))

def is_button_hovered(rect):
    mouse_pos = pygame.mouse.get_pos()  # Get mouse position
    return rect.collidepoint(mouse_pos)  # Check if mouse is over the button

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # sys.exit()
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the click occurred within the button's rectangle
            if beginner_button.collidepoint(pygame.mouse.get_pos()):
                # Perform an action here
                main.run_main(button_text)
                pygame.quit()
            elif inter_button.collidepoint(pygame.mouse.get_pos()):
                main.run_main(button_text_2)
                pygame.quit()
            elif professional_button.collidepoint(pygame.mouse.get_pos()):
                main.run_main(button_text_3)
                pygame.quit()
            elif expert_button.collidepoint(pygame.mouse.get_pos()):
                main.run_main(button_text_4)
                pygame.quit()

    if is_button_hovered(beginner_button):
        draw_button(SCREEN, beginner_button, button_hover_color, button_text)
    elif is_button_hovered(inter_button):
        draw_button(SCREEN, inter_button, button_hover_color, button_text_2)
    elif is_button_hovered(professional_button):
        draw_button(SCREEN, professional_button, button_hover_color, button_text_3)
    elif is_button_hovered(expert_button):
        draw_button(SCREEN, expert_button, button_hover_color, button_text_4)
    else:
        draw_button(SCREEN, beginner_button, button_color, button_text)
        draw_button(SCREEN, inter_button, button_color, button_text_2)
        draw_button(SCREEN, professional_button, button_color, button_text_3)
        draw_button(SCREEN, expert_button, button_color, button_text_4)

    # pygame.display.update()
    pygame.display.flip()

pygame.quit()

