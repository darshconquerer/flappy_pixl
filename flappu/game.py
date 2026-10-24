import pygame
from sys import exit
import random

pygame.init()
screen = pygame.display.set_mode((1000, 500))
pygame.display.set_caption('Flappy')

font_ = pygame.font.Font(None, 50)

bg_img = pygame.image.load('./flappu/graphics/Bg.png').convert_alpha()
bg_img = pygame.transform.scale(bg_img, (1000, 500))
bg_width = bg_img.get_width()
bg_x_axis = 0

char_img = pygame.image.load('./flappu/graphics/tremp.png').convert_alpha()
char_img = pygame.transform.scale(char_img ,(100, 100))
char_img_rect = char_img.get_rect(midbottom = (250, 150))

pipe_u_img = pygame.image.load('./flappu/graphics/Up.png').convert_alpha()
pipe_d_img = pygame.image.load('./flappu/graphics/Down.png').convert_alpha()

pipe_w = pipe_d_img.get_width()
pipe_u_img = pygame.transform.scale(pipe_u_img, (pipe_w, 500)).convert_alpha()
pipe_d_img = pygame.transform.scale(pipe_d_img, (pipe_w, 500)).convert_alpha()

char_mask = pygame.mask.from_surface(char_img)
pipe_u_mask = pygame.mask.from_surface(pipe_u_img)
pipe_d_mask = pygame.mask.from_surface(pipe_d_img)

pipe_u_rect= []
pipe_d_rect = []

SPACE = 400
num_pipes = 3
scored = [False]*num_pipes
score = 0

for n in range(num_pipes):
    starting_point = 1000 + n*SPACE
    gap_size = random.randint(110, 150)
    gap_center = random.randint(150, 280)

    half_gap = gap_size//2

    pipe_d_rect.append(pipe_d_img.get_rect(midbottom = (starting_point, gap_center - half_gap)))
    pipe_u_rect.append(pipe_u_img.get_rect(midtop = (starting_point, gap_center + half_gap)))

scroll = 7
gravity = 0.25
speed = 0
jump = -5

landing_screen = True
game_play = False

landing_img = pygame.image.load('./flappu/graphics/Bg_land.png').convert()
landing_img = pygame.transform.scale(landing_img, (1000, 500))

rect_play = pygame.Rect(0, 0, 200, 60)
rect_play.center = (500, 250)

play_game_text_img = pygame.image.load('./flappu/graphics/play_text.png').convert_alpha()
play_game_text_img = pygame.transform.scale(play_game_text_img, (160, 60))
rect_play_game_text_img = play_game_text_img.get_rect(center=rect_play.center)

enter_game_img = pygame.image.load('./flappu/graphics/enter_game.png') 
enter_game_img = pygame.transform.scale(enter_game_img, (250, 75))
enter_game_rect = enter_game_img.get_rect(midleft =(380, 390))
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
                    landing_screen = False
                    game_play = True
            if events.type == pygame.KEYDOWN:
                 if(events.key == pygame.K_SPACE):
                    landing_screen = False
                    game_play = True    

    if game_play: 
        bg_x_axis -= scroll
        if bg_x_axis <= -bg_width:
            bg_x_axis = 0

        speed += gravity
        char_img_rect.y += speed

        if char_img_rect.y > 490 or char_img_rect.y < -50:
            char_img_rect.y = 150
            speed = 0
            score = 0
            game_play = False

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
                gap_size = random.randint(60, 100)
                gap_center = random.randint(120, 400)
                half_gap = gap_size//2

                other_pipe = (i-1) % num_pipes

                new_pipe_x = pipe_d_rect[other_pipe].centerx + SPACE

                pipe_d_rect[i].midbottom = (new_pipe_x, gap_center - half_gap)
                pipe_u_rect[i].midtop = (new_pipe_x, gap_center + half_gap)

                scored[i] = False
            
            img_u_correct = (pipe_u_rect[i].x - char_img_rect.x, pipe_u_rect[i].y - char_img_rect.y)
            img_d_correct = (pipe_d_rect[i].x - char_img_rect.x, pipe_d_rect[i].y - char_img_rect.y)

            if char_mask.overlap(pipe_u_mask, img_u_correct) or char_mask.overlap(pipe_d_mask, img_d_correct):
                char_img_rect.center = (300, 200)
                speed = 0
                score = 0
                game_play = False


            screen.blit(pipe_u_img, pipe_u_rect[i])
            screen.blit(pipe_d_img, pipe_d_rect[i])

        score_flap = font_.render(str(score), True, 'white')
        screen.blit(score_flap, (475, 40))

    elif landing_screen:
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        screen.blit(landing_img, (0, 0))
        screen.blit(play_button_img, rect_play)
        screen.blit(play_game_text_img, rect_play_game_text_img)
        screen.blit(enter_game_img, (enter_game_rect))
        pygame.draw.rect(screen, WHITE, rect_play, 1)
        
    pygame.display.update()
    clock.tick(60)
