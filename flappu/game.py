import pygame
from sys import exit
import random

pygame.init()
screen = pygame.display.set_mode((1000, 500))
pygame.display.set_caption('Flappy')

font_ = pygame.font.Font(None, 50)

score = 0
scored = [False, False]

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
pipe_u_img = pygame.transform.scale(pipe_u_img, (pipe_w, 500))
pipe_d_img = pygame.transform.scale(pipe_d_img, (pipe_w, 500))

pipe_u_rect= []
pipe_d_rect = []

SPACE = 800

for starting_point in [1000, 1000 + SPACE]:
    gap_size = random.randint(110, 150)
    gap_center = random.randint(150, 280)

    half_gap = gap_size//2

    pipe_d_rect.append(pipe_d_img.get_rect(midbottom = (starting_point, gap_size - half_gap)))
    pipe_u_rect.append(pipe_u_img.get_rect(midtop = (starting_point, gap_size + half_gap)))

scroll = 7
gravity = 0.25
speed = 0
jump = -5

landing_screen = True
game_play = False

landing_img = pygame.image.load('./flappu/graphics/Bg_land.png')
landing_img = pygame.transform.scale(landing_img, (1000, 500))

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

        char_collision_box = char_img_rect.inflate(-98, -88)

        for i in range(2):
            pipe_d_rect[i].x -= scroll
            pipe_u_rect[i].x -= scroll

            if not scored[i] and pipe_d_rect[i].right < char_img_rect.centerx:
                        score += 1
                        scored[i] = True

            if pipe_d_rect[i].right < 0:
                gap_size = random.randint(60, 100)
                gap_center = random.randint(120, 400)
                half_gap = gap_size//2

                other_pipe = (i+1) % 2

                new_pipe_x = pipe_d_rect[other_pipe].centerx + SPACE

                pipe_d_rect[i].midbottom = (new_pipe_x, gap_center - half_gap)
                pipe_u_rect[i].midtop = (new_pipe_x, gap_center + half_gap)

                scored[i] = False
            
            pipe_u_colliosion_box = pipe_u_rect[i].inflate(-124, 0)
            pipe_d_colliosion_box = pipe_d_rect[i].inflate(-124, 0)

            if(char_collision_box.colliderect(pipe_u_colliosion_box) or char_collision_box.colliderect(pipe_d_colliosion_box)):
                char_img_rect.center = (300, 200)
                speed = 0
                score = 0
                game_play = False

                pipe_u_rect[0].x = 1000
                pipe_d_rect[0].x = 1000
                pipe_u_rect[1].x = 1000 + SPACE
                pipe_d_rect[1].x = 1000 + SPACE

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

    pygame.display.update()
    clock.tick(60)
