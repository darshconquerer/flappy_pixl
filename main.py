import pygame
import random
import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def score_path():
    return os.path.join(os.path.expanduser("~"), ".flappy_highscore.txt")

def log_crash(exc_type, exc_value, exc_tb):
    import traceback
    try:
        with open(os.path.join(os.path.expanduser("~"), "flappy_crash.log"), "w") as f:
            traceback.print_exception(exc_type, exc_value, exc_tb, file=f)
    except OSError:
        pass
    if sys.stderr is not None:
        sys.__excepthook__(exc_type, exc_value, exc_tb)
 
sys.excepthook = log_crash

pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('Flappy')

font_ = pygame.font.Font(None, 72)
hint_font = pygame.font.Font(None, 36)
btn_font = pygame.font.Font(None, 40)
small_font = pygame.font.Font(None, 28)

WHITE = (255, 255, 255)
GOLD = (255, 215, 0)

def draw_text(text, font, center, color = WHITE):
    surf = font.render(text, True, color)
    screen.blit(surf, surf.get_rect(center = center))

bg_img = pygame.image.load(resource_path("graphics/Bg.png")).convert()
bg_img = pygame.transform.scale(bg_img, (1280, 720))
bg_width = bg_img.get_width()
bg_height = bg_img.get_height()
bg_x_axis = 0
bg_y_axis = 0

char_files = ['graphics/tremp.png', 'graphics/putin.png', 'graphics/xi.png']
char_imgs = []
char_masks = []

for f in char_files:
    img = pygame.image.load(resource_path(f)).convert_alpha()
    img = pygame.transform.scale(img, (144, 144))
    char_imgs.append(img)
    char_masks.append(pygame.mask.from_surface(img))

selected = 0
char_img = char_imgs[selected]
char_mask = char_masks[selected]
char_img_rect = char_img.get_rect(midbottom = (320, 216))

def select_char(index):
    global selected, char_img, char_mask
    selected = index % len(char_imgs)
    char_img = char_imgs[selected]
    char_mask = char_masks[selected]

pipe_u_img = pygame.image.load(resource_path('graphics/Up.png')).convert_alpha()
pipe_d_img = pygame.image.load(resource_path('graphics/Down.png')).convert_alpha()

pipe_w = pipe_d_img.get_width()*1.28
pipe_u_img = pygame.transform.scale(pipe_u_img, (pipe_w, 730)).convert_alpha()
pipe_d_img = pygame.transform.scale(pipe_d_img, (pipe_w, 730)).convert_alpha()

pipe_u_mask = pygame.mask.from_surface(pipe_u_img)
pipe_d_mask = pygame.mask.from_surface(pipe_d_img)

pipe_u_rect= []
pipe_d_rect = []

SPACE = 614
num_pipes = 3
scored = [False]*num_pipes
score = 0

final_score = 0
high_score = 0
try:
    with open(score_path()) as hs_file:
        high_score = int(hs_file.read())
except (FileNotFoundError, ValueError):
    pass
for n in range(num_pipes):
    starting_point = 1280 + n*SPACE
    gap_size = random.randint(173, 216)
    gap_center = random.randint(216, 403)

    half_gap = gap_size//2

    pipe_d_rect.append(pipe_d_img.get_rect(midbottom = (starting_point, gap_center - half_gap)))
    pipe_u_rect.append(pipe_u_img.get_rect(midtop = (starting_point, gap_center + half_gap)))

def save_scores():
    global final_score, high_score
    if not game_play:
        return
    final_score = score
    if score> high_score:
        high_score = score
        try:
            with open(score_path(), 'w') as hs_file:
                hs_file.write(str(high_score))
        except OSError: pass

base_scroll = 8

difficulties = [
    ('Very Easy', 0.5),
    ('Easy', 0.75),
    ('Normal', 1.0),
    ('Good', 1.15),
    ('Hard', 1.25),
    ('Insane', 1.35),
    ('Impossible', 1.6)
]

difficulty_index = 1
scroll = round(base_scroll * difficulties[1][1])

diff_label = 'Select Difficulty'

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
diff_select = False
game_over = False

def show_screen(name):
    global landing_screen, diff_select, game_play, game_over
    landing_screen = (name == 'landing')
    diff_select = (name == 'diff_select')
    game_play = (name == 'play')
    game_over = (name == 'game_over')

landing_img = pygame.image.load(resource_path('graphics/Bg_land.png')).convert()
landing_img = pygame.transform.scale(landing_img, (1280, 720))
landing_img_width = landing_img.get_width()
landing_img_x = 0

rect_play = pygame.Rect(0, 0, 256, 86)
rect_diff = pygame.Rect(0, 0, 256, 86)
rect_play.center = (640, 360)
rect_diff.center = (640, 500)

rect_play1 = pygame.Rect(0, 0, 256, 86)
rect_play2 = pygame.Rect(0, 0, 256, 86)
rect_play1.center = (640, 288)
rect_play2.center = (640, 432)

rect_back = pygame.Rect(0, 0, 256, 86)
rect_left = pygame.Rect(0, 0, 90, 90)
rect_right = pygame.Rect(0, 0, 90, 90)
rect_back.center = (640, 600)
rect_left.center = (420, 320)
rect_right.center = (860, 320)

diff_rects = []
for i in range(len(difficulties)):
    r = pygame.Rect(0, 0, 256, 86)
    r.center = (490 + (i%2)* 300, 180 + (i//2)*95)
    diff_rects.append(r)

play_game_text_img = pygame.image.load(resource_path('graphics/play_text.png')).convert_alpha()
play_game_text_img = pygame.transform.scale(play_game_text_img, (230, 86))
rect_play_game_text_img = play_game_text_img.get_rect(center=rect_play.center)

enter_game_img = pygame.image.load(resource_path('graphics/enter_game.png')).convert_alpha()
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

play_again_img = pygame.image.load(resource_path('graphics/play_again.png')).convert_alpha()
main_menu_img = pygame.image.load(resource_path('graphics/main_menu.png')).convert_alpha()

play_again_img = pygame.transform.scale(play_again_img, (230, 86))
rect_play_again_img = play_again_img.get_rect(center=rect_play1.center)
main_menu_img = pygame.transform.scale(main_menu_img, (230, 86))
rect_main_menu_img = main_menu_img.get_rect(center=rect_play2.center)

def draw_button(rect, border = WHITE, width = 1):
    screen.blit(pygame.transform.scale(play_button_img, rect.size), rect)
    pygame.draw.rect(screen, border, rect, width)

clock = pygame.time.Clock()
while True:
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game_play:
            if events.type == pygame.KEYDOWN:
                if events.key == pygame.K_SPACE:
                    speed = jump 

        elif landing_screen:
            if(events.type == pygame.MOUSEBUTTONDOWN):
                if rect_play_game_text_img.collidepoint(events.pos):
                    reset_game()
                    landing_screen = False
                    game_play = True
                    game_over = False
                elif rect_diff.collidepoint(events.pos):
                    show_screen('diff_select')
            if events.type == pygame.KEYDOWN:
                if(events.key == pygame.K_SPACE):
                    reset_game()
                    landing_screen = False
                    game_play = True 
                    game_over = False  
                if events.key == pygame.K_RETURN:
                    reset_game()
                    landing_screen = False
                    game_play = True 
                    game_over = False 
                if(events.key) == pygame.K_RIGHT or events.key == pygame.K_d:
                    select_char(selected + 1)
                if events.key == pygame.K_LEFT or events.key == pygame.K_a:
                    select_char(selected - 1)
        
        elif diff_select:
            if events.type == pygame.MOUSEBUTTONDOWN:
                for i in range (len(diff_rects)):
                    if diff_rects[i].collidepoint(events.pos):
                        difficulty_index = i 
                        diff_label = difficulties[i][0]
                        scroll = int(base_scroll * difficulties[i][1])
                        show_screen('landing')  
                if rect_back.collidepoint(events.pos):
                    show_screen('landing')

        elif(game_over):
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
            save_scores()
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
                gap_size = random.randint(70 , 150)
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
                save_scores()
                speed = 0
                score = 0

                game_play = False
                game_over = True
                landing_screen = False

            screen.blit(pipe_u_img, pipe_u_rect[i])
            screen.blit(pipe_d_img, pipe_d_rect[i])

        score_flap = font_.render(str(score), True, 'white')
        screen.blit(score_flap, (608, 58))

    elif landing_screen or diff_select:
        landing_img_x -= base_scroll // 3
        if landing_img_x <= -landing_img_width:
            landing_img_x = 0

        screen.blit(landing_img, (landing_img_x, 0))
        screen.blit(landing_img, (landing_img_x + landing_img_width , 0))

        if landing_screen:
            screen.blit(play_button_img, rect_play)
            screen.blit(play_game_text_img, rect_play_game_text_img)
            pygame.draw.rect(screen, WHITE, rect_play, 1)
            screen.blit(enter_game_img, (enter_game_rect))

            draw_button(rect_diff)
            draw_text(diff_label, btn_font, rect_diff.center)

            preview_rect = char_img.get_rect(center = (640, 190))
            screen.blit(char_img, preview_rect)

            preview_rect = char_img.get_rect(center = (640, 190))
            screen.blit(char_img, preview_rect)

            hint = hint_font.render('Press A or D to change character', True, 'white')
            screen.blit(hint, hint.get_rect(center = (640, 50)))


        elif diff_select:
            draw_text('Select Difficulty', font_, (640, 70))

            for i in range(len(difficulties)):
                name, mult = difficulties[i]
                if i == difficulty_index:
                    draw_button(diff_rects[i], GOLD, 4) 
                else:
                    draw_button(diff_rects[i])
                draw_text(name, btn_font, (diff_rects[i].centerx, diff_rects[i].centery - 12))
                draw_text(str(mult) + 'x', small_font, (diff_rects[i].centerx, diff_rects[i].centery + 20))

                draw_button(rect_back)
                draw_text('Back', btn_font, rect_back.center)

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

        draw_text('Score: ' + str(final_score), font_, (640, 70))
        draw_text('High Score: ' + str(high_score), font_, (640, 150), GOLD)

    pygame.display.update()
    clock.tick(60)
