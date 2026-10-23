import pygame
from sys import exit

screen = pygame.display.set_mode((1000, 500))
pygame.display.set_caption('Flappy')

bg_img = pygame.image.load('./flappu/graphics/Bg.png').convert_alpha()
bg_img = pygame.transform.scale(bg_img, (1000, 500))
bg_width = bg_img.get_width();
bg_x_axis = 0

char_img = pygame.image.load('./flappu/graphics/tremp.png').convert_alpha()
char_img = pygame.transform.scale(char_img ,(100, 100))
char_img_rect = char_img.get_rect(midbottom = (250, 150))

pipe_u_img = pygame.image.load('./flappu/graphics/Up.png').convert_alpha()
pipe_d_img = pygame.image.load('./flappu/graphics/Down.png').convert_alpha()
pipe_u_rect = pipe_u_img.get_rect(midtop = (1000, 400))
pipe_d_rect = pipe_d_img.get_rect(midbottom = (1000, 250))

scroll = 7
gravity = 0.25
speed = 0
jump = -5
clock = pygame.time.Clock()
while True:
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            pygame.quit()
            exit()
        if events.type == pygame.KEYDOWN:
            if events.key == pygame.K_SPACE:
                speed = jump 
        
    bg_x_axis -= scroll
    if bg_x_axis <= -bg_width:
        bg_x_axis = 0

    speed += gravity
    char_img_rect.y += speed

    if char_img_rect.y > 490 or char_img_rect.y < -50:
        char_img_rect.y = 150
        speed = 0

    pipe_d_rect.x -= scroll
    pipe_u_rect.x -= scroll

    if pipe_u_rect.x < -175:
        pipe_u_rect.x = 1000
        pipe_d_rect.x = 1000

    screen.blit(bg_img, (bg_x_axis, 0))
    screen.blit(bg_img, (bg_x_axis+ bg_width, 0))
    screen.blit(char_img, char_img_rect)
    screen.blit(pipe_u_img, pipe_u_rect)
    screen.blit(pipe_d_img, pipe_d_rect)

    pygame.display.update()
    clock.tick(60)
