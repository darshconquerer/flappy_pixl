import pygame
from sys import exit
import random

pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('Flappy')

font_ = pygame.font.Font(None, 72)
bg_img = pygame.image.load('graphics/Bg.png').convert()
bg_img = pygame.transform.scale(bg_img, (1280, 720))
bg_width = bg_img.get_width()
bg_height = bg_img.get_height()
bg_x_axis = 0
bg_y_axis = 0

char_img = pygame.image.load('graphics/tremp.png').convert_alpha()
char_img = pygame.transform.scale(char_img ,(144, 144))
char_img_rect = char_img.get_rect(midbottom = (320, 216))

pipe_u_img = pygame.image.load('graphics/Up.png').convert_alpha()
pipe_d_img = pygame.image.load('graphics/Down.png').convert_alpha()

pipe_w = pipe_d_img.get_width()*1.28
pipe_u_img = pygame.transform.scale(pipe_u_img, (pipe_w, 730)).convert_alpha()
pipe_d_img = pygame.transform.scale(pipe_d_img, (pipe_w, 730)).convert_alpha()

char_mask = pygame.mask.from_surface(char_img)
pipe_u_mask = pygame.mask.from_surface(pipe_u_img)
pipe_d_mask = pygame.mask.from_surface(pipe_d_img)

pipe_u_rect= []
pipe_d_rect = []

SPACE = 614
num_pipes = 3
scored = [False]*num_pipes
score = 0

for n in range(num_pipes):
    starting_point = 1280 + n*SPACE
    gap_size = random.randint(173, 216)
    gap_center = random.randint(216, 403)

    half_gap = gap_size//2

    pipe_d_rect.append(pipe_d_img.get_rect(midbottom = (starting_point, gap_center - half_gap)))
    pipe_u_rect.append(pipe_u_img.get_rect(midtop = (starting_point, gap_center + half_gap)))

scroll = 8
gravity = 0.36
speed = 0
jump = -7.9

def reset_game():
    global score, speed, bg_x_axis
    score = 0
    speed = 0
    bg_x_axis = 0
    char_img_rect.midbottom = (320, 216)

    for n in range(num_pipes):
        starting_point = 1280 + n*SPACE
        gap_size = random.randint(110, 180)
        gap_center = random.randint(216, 403)

        half_gap = gap_size//2

        pipe_d_rect[n].midbottom = (starting_point, gap_center - half_gap)
        pipe_u_rect[n].midtop = (starting_point, gap_center + half_gap)

        scored[n] = False

landing_screen = True
game_play = False
game_over = False
landing_img = pygame.image.load('graphics/Bg_land.png').convert()
landing_img = pygame.transform.scale(landing_img, (1280, 720))
landing_img_width = landing_img.get_width()
landing_img_x = 0

rect_play = pygame.Rect(0, 0, 256, 86)
rect_play1 = pygame.Rect(0, 0, 256, 86)
rect_play2 = pygame.Rect(0, 0, 256, 86)
rect_play.center = (640, 360)
rect_play1.center = (640, 288)
rect_play2.center = (640, 432)

play_game_text_img = pygame.image.load('graphics/play_text.png').convert_alpha()
play_game_text_img = pygame.transform.scale(play_game_text_img, (230, 86))
rect_play_game_text_img = play_game_text_img.get_rect(center=rect_play.center)

enter_game_img = pygame.image.load('graphics/enter_game.png').convert_alpha()
enter_game_img = pygame.transform.scale(enter_game_img, (360, 108))
enter_game_rect = enter_game_img.get_rect(midleft =(466, 662))
WHITE = (255, 255, 255)

block = 10

block_w = rect_play.width
block_h = rect_play.height
px_img = pygame.Surface((block_w, block_h))

for x in range (block_w):
    for y in range (block_h):

            s = random.randint(90, 190)

            px_img.set_at((x, y), (s, s, s))
play_button_img = pygame.transform.scale(px_img, rect_play.size)

play_again_img = pygame.image.load('graphics/play_again.png').convert_alpha()
main_menu_img = pygame.image.load('graphics/main_menu.png').convert_alpha()

play_again_img = pygame.transform.scale(play_again_img, (230, 86))
rect_play_again_img = play_again_img.get_rect(center=rect_play1.center)
main_menu_img = pygame.transform.scale(main_menu_img, (230, 86))
rect_main_menu_img = main_menu_img.get_rect(center=rect_play2.center)


clock = pygame.time.Clock()
while True:
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_play:
            if events.type == pygame.KEYDOWN:
                if events.key == pygame.K_SPACE:
                    speed = jump 

        if landing_screen:
            if(events.type == pygame.MOUSEBUTTONDOWN):
                if rect_play_game_text_img.collidepoint(events.pos):
                    reset_game()
                    landing_screen = False
                    game_play = True
                    game_over = False
            if events.type == pygame.KEYDOWN:
                if(events.key == pygame.K_SPACE):
                    reset_game()
                    landing_screen = False
                    game_play = True 
                    game_over = False   

        if(game_over):
            if events.type == pygame.MOUSEBUTTONDOWN:
                if rect_main_menu_img.collidepoint(events.pos):
                    landing_screen = True
                    game_over = False
                    game_play = False

                if rect_play_again_img.collidepoint(events.pos):
                    reset_game()
                    landing_screen = False
                    game_over = False
                    game_play = True
            
    if game_play: 
        bg_x_axis -= scroll
        if bg_x_axis <= -bg_width:
            bg_x_axis = 0

        speed += gravity
        char_img_rect.y += speed

        if char_img_rect.y > 706 or char_img_rect.y < -72:
            char_img_rect.y = 216
            speed = 0
            score = 0
            game_play = False
            landing_screen = False
            game_over = True

        screen.blit(bg_img, (bg_x_axis, 0))
        screen.blit(bg_img, (bg_x_axis+ bg_width, 0))
        screen.blit(char_img, char_img_rect)

        for i in range(num_pipes):
            pipe_d_rect[i].x -= scroll
            pipe_u_rect[i].x -= scroll

            if not scored[i] and pipe_d_rect[i].right < char_img_rect.centerx:
                        score += 1
                        scored[i] = True

            if pipe_d_rect[i].right < 0:
                gap_size = random.randint(80 , 150)
                gap_center = random.randint(200, 550)
                half_gap = gap_size//2

                other_pipe = (i-1) % num_pipes

                new_pipe_x = pipe_d_rect[other_pipe].centerx + SPACE

                pipe_d_rect[i].midbottom = (new_pipe_x, gap_center - half_gap)
                pipe_u_rect[i].midtop = (new_pipe_x, gap_center + half_gap)

                scored[i] = False
            
            img_u_correct = (pipe_u_rect[i].x - char_img_rect.x, pipe_u_rect[i].y - char_img_rect.y)
            img_d_correct = (pipe_d_rect[i].x - char_img_rect.x, pipe_d_rect[i].y - char_img_rect.y)

            if char_mask.overlap(pipe_u_mask, img_u_correct) or char_mask.overlap(pipe_d_mask, img_d_correct):
                char_img_rect.center = (384, 288)
                speed = 0
                score = 0

                game_play = False
                game_over = True
                landing_screen = False

            screen.blit(pipe_u_img, pipe_u_rect[i])
            screen.blit(pipe_d_img, pipe_d_rect[i])

        score_flap = font_.render(str(score), True, 'white')
        screen.blit(score_flap, (608, 58))

    elif landing_screen:
        landing_img_x -= scroll // 3
        if landing_img_x <= -landing_img_width:
            landing_img_x = 0

        screen.blit(landing_img, (landing_img_x, 0))
        screen.blit(landing_img, (landing_img_x + landing_img_width , 0))
        screen.blit(play_button_img, rect_play)
        screen.blit(play_game_text_img, rect_play_game_text_img)
        screen.blit(enter_game_img, (enter_game_rect))
        pygame.draw.rect(screen, WHITE, rect_play, 1)

    elif game_over:
        bg_y_axis -= scroll // 2
        if bg_y_axis <= -bg_height:
            bg_y_axis = 0

        screen.blit(bg_img, (0, bg_y_axis))
        screen.blit(bg_img, (0, bg_y_axis + bg_height))
        screen.blit(play_button_img, rect_play1)
        screen.blit(play_button_img, rect_play2)
        screen.blit(play_again_img, rect_play_again_img)
        screen.blit(main_menu_img, rect_main_menu_img)
        pygame.draw.rect(screen, WHITE, rect_play1, 1)
        pygame.draw.rect(screen, WHITE, rect_play2, 1)

    pygame.display.update()
    clock.tick(60)

