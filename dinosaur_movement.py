current_time = pygame.time.get_ticks()
if current_time - last_update >= animation_cooldown:
    frame += 1
    last_update = current_time
    if frame >= len(animation_list):
        frame = 0
    if flag % 2 == 0:
        if x_con < 36 and y_con > 35 and dice > 0:
            y_con -= 1
            dice -= 1
        if x_con > 34 and y_con < 36 and dice > 0:
            x_con += 1
            dice -= 1
        if x_con > 699 and y_con < 700 and dice > 0:
            y_con += 1
            dice -= 1
        if x_con > 34 and y_con > 699 and dice > 0:
            x_con -= 1
            dice -= 1

print(x_con, y_con)

SCREEN.blit(animation_list[frame], (x_con, y_con))





ug = 0
lg = 400

# screen = pygame.display.set_mode((Screen_width, Screen_height))
# pygame.display.set_caption('Spritesheets')

sprite_sheet_image = pygame.image.load('doux.png').convert_alpha()
sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)
animation_list = []
last_update = pygame.time.get_ticks()
animation_cooldown = 10
frame = 0
step_counter = 0
x_con = 35
y_con = 700
flag = 2
x = 5
dice = 100000
# small =100 large =133


for x in range(5, 11):
    animation_list.append(sprite_sheet.get_image(x, 24, 24, 3, colors.CREAM_COLOR))
