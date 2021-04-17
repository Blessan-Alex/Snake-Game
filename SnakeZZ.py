import pygame
import random
import os

pygame.init()

# colours
window_width = 800
window_height = 600
white = (255, 255, 255)
red = (255, 0, 0)
purple = (255, 0, 255)
dark_red = (153, 0, 0)
dark_blue = (0, 0, 50)
green = (0, 204, 0)
light_blue = (0, 255, 255)
dark_purple = (60, 25, 60)
light_red = (255, 51, 51)

window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("SnakeZZ")

clock = pygame.time.Clock()


# images
game_over_img = pygame.image.load("Assets/Snake/game_over3.png")
game_over_img = pygame.transform.scale(game_over_img, (550, 550))
glass_img = pygame.image.load("Assets/Snake/glasses.png")
glass_img = pygame.transform.scale(glass_img, (25, 25))


# sounds
food_sound = pygame.mixer.Sound('Assets/Snake/food_eat.wav')
game_over_sound = pygame.mixer.Sound('Assets/Snake/game_over.wav')


# fonts
pixel_font = pygame.font.Font('Assets/Fonts/pixel.ttf', 25)
chess_font = pygame.font.Font('Assets/Fonts/Chess.ttf', 25)
play_font = pygame.font.Font('Assets/Fonts/Chess.ttf', 35)
start_font = pygame.font.Font('Assets/Fonts/Chess.ttf', 100)


def plot_text(font, text, colour, x, y):
    screen_text = font.render(text, True, colour)
    window.blit(screen_text, [x, y])


def plot_snake(window, colour, snake_list, snake_width, snake_height):
    for x, y in snake_list:
        pygame.draw.rect(window, colour, [x, y, snake_width, snake_height])


def draw_rect(window, colour, x, y, width, height):
    pygame.draw.rect(window, colour, [x, y, width, height])


def welcome():
    x = 300
    y = 250
    exit_game = False

    music = pygame.mixer.music.load('Assets/Snake/Game_menu.mp3')
    pygame.mixer.music.play(-1)

    while not exit_game:

        window.fill(dark_purple)

        plot_text(start_font, "SnakeZZ", light_blue, 150, 100)
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if x <= mouse[0] <= x+140 and y <= mouse[1] <= y+40:
                    game()
                if x <= mouse[0] <= x+140 and y+60 <= mouse[1] <= y+40+60:
                    exit_game = True
        if x <= mouse[0] <= x+140 and y <= mouse[1] <= y+40:
            draw_rect(window, light_red, x, y, 140, 40)
        else:
            draw_rect(window, red, x, y, 140, 40)

        if x <= mouse[0] <= x+140 and y+60 <= mouse[1] <= y+40+60:
            draw_rect(window, light_red, x, y+60, 140, 40)
        else:
            draw_rect(window, red, x, y+60, 140, 40)

        plot_text(play_font, 'Play', light_blue, x+28, y+1)
        plot_text(play_font, 'Quit', light_blue, x+28, y+61)

        pygame.display.update()
        clock.tick(60)


def game():
    music = pygame.mixer.music.load('Assets/Snake/background.mp3')
    pygame.mixer.music.play(-1)

    if(not os.path.exists("highscore.txt")):
        with open("highscore.txt", "w") as f:
            f.write("0")

    exit_game = False
    game_over = False
    snake_x = 100
    snake_y = 100
    vel_x = 0
    vel_y = 0
    snake_list = []
    snake_length = 1
    score = 0
    snake_width = 18
    snake_height = 17
    initial_vel = 1.5
    fps = 60
    food_width = 14
    food_height = 14
    highscore = 0
    with open("highscore.txt", "r") as f:
        highscore = f.read()
    food_x = random.randint(20, window_width - 100)
    food_y = random.randint(100, window_height - 100)

    while not exit_game:

        if game_over:
            pygame.mixer.music.stop()
            game_over_sound.play()

            with open("highscore.txt", "w") as f:
                f.write(str(highscore))
            window.blit(game_over_img, (120, -10))
            plot_text(chess_font, "Press Enter To Restart", purple, 220, 500)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        vel_x = initial_vel
                        vel_y = 0
                    if event.key == pygame.K_LEFT:
                        vel_x = -initial_vel
                        vel_y = 0
                    if event.key == pygame.K_DOWN:
                        vel_y = initial_vel
                        vel_x = 0
                    if event.key == pygame.K_UP:
                        vel_y = -initial_vel
                        vel_x = 0
            snake_x += vel_x
            snake_y += vel_y

            hit_box_snake = (snake_x, snake_y + 2,
                             snake_width - 5, snake_height - 5)
            hit_box_food = (food_x-3, food_y - 5,
                            food_width - 4, food_height - 4)

            if hit_box_snake[1] < hit_box_food[1]+hit_box_food[3] and hit_box_snake[1] + hit_box_snake[3] > hit_box_food[1]:
                if hit_box_snake[0] + hit_box_snake[2] > hit_box_food[0] and hit_box_snake[0] < hit_box_food[0]+hit_box_food[2]:
                    food_sound.play()
                    score += 10
                    snake_length += 4
                    initial_vel += 0.1
                    food_x = random.randint(20, window_width - 100)
                    food_y = random.randint(100, window_height - 100)

            if score > int(highscore):
                highscore = score
            head = []
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)

            # if head in snake_list[:-2]:
            #game_over = True

            if len(snake_list) > snake_length:
                del snake_list[0]

            if snake_x < 10 or snake_x > window_width-25 or snake_y < 44.5 or snake_y > window_height-24:
                game_over = True

            snake_rect = pygame.Rect(
                snake_x, snake_y, snake_width, snake_height)

            obstacle2_rect = pygame.Rect(3, 200, 250, 10)
            obstacle3_rect = pygame.Rect(550, 380, 250, 10)
            obstacle4_rect = pygame.Rect(400, 40, 10, 200)
            obstacle5_rect = pygame.Rect(400, 400, 10, 196)

            food_box = pygame.Rect(hit_box_food)
            if food_box.colliderect(obstacle2_rect) or food_box.colliderect(obstacle3_rect) or food_box.colliderect(obstacle4_rect) or food_box.colliderect(obstacle5_rect):
                food_x = random.randint(20, window_width - 100)
                food_y = random.randint(100, window_height - 100)

            if snake_rect.colliderect(obstacle2_rect) or snake_rect.colliderect(obstacle3_rect) or snake_rect.colliderect(obstacle4_rect) or snake_rect.colliderect(obstacle5_rect):
                game_over = True

            window.fill(dark_blue)
            pygame.draw.line(window, light_blue, (1, 40),
                             (window_width, 40), width=5)
            pygame.draw.line(window, light_blue, (1, window_height-2.5),
                             (window_width, window_height-2.5), width=5)
            pygame.draw.line(window, light_blue, (1, 38),
                             (1, window_height), width=5)
            pygame.draw.line(window, light_blue, (window_width-2,
                                                  38), (window_width-2, 600), width=5)
            # pygame.draw.rect(window,red,hit_box_snake,1)
            # pygame.draw.rect(window,red,hit_box_food,1)
            draw_rect(window, light_blue, 3, 200, 250, 10)
            draw_rect(window, light_blue, 550, 380, 250, 10)
            draw_rect(window, light_blue, 400, 40, 10, 200)
            draw_rect(window, light_blue, 400, 400, 10, 196)
            plot_text(chess_font, "HighScore: " + str(highscore) +
                      "           Score: "+str(score), white, 5, 5)
            plot_snake(window, red, snake_list, snake_width, snake_height)
            pygame.draw.circle(window, green, (food_x, food_y), 8)
            window.blit(glass_img, (snake_x-4, snake_y-7))

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()


welcome()
