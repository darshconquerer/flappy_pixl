import pygame
from sys import exit

screen = pygame.display.set_mode((1000, 500))
pygame.display.set_caption('Flappy')

bg_img = pygame.image.load('./graphics/Bg.PNG')
bg_img = pygame.transform.scale(bg_img, (1000, 500))
bg_width = bg_img.get_width();
bg_x_axis = 0

char_img = pygame.image.load('./graphics/tremp.png')
char_img = pygame.transform.scale(char_img ,(100, 100))

scroll = 2
clock = pygame.time.Clock()
while True:
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            pygame.quit()
            exit()

    bg_x_axis -= scroll
    if bg_x_axis <= -bg_width:
        bg_x_axis = 0

    screen.blit(bg_img, (bg_x_axis, 0))
    screen.blit(bg_img, (bg_x_axis+ bg_width, 0))
    screen.blit(char_img, (300, 250))
    pygame.display.update()
    clock.tick(60)
