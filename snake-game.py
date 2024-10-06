import pygame
import random
import os
import json 


working_directory = os.path.realpath(__file__).strip("snake-game.py")
asset_fp = working_directory + "/assets/"


pygame.init()

#visual parameters 
black = (0, 0, 0)
green = (184, 213, 68)

dis_width = 800
dis_height = 600
borderbuffer = 40

dis = pygame.display.set_mode((dis_width, dis_height))
clock = pygame.time.Clock()

snake_block = 10
snake_speed = 15

font_fp = asset_fp + "nokiafc22.ttf"
font_style = pygame.font.Font(font_fp, 25)
high_score_fp = asset_fp + "high_score.json"

def load_high_score():
    try:
        with open(high_score_fp, 'r') as f:
            return json.load(f)['high_score']
    except (FileNotFoundError, json.JSONDecodeError):
        save_high_score(0)
        return 0 

def save_high_score(score): #saves high score for future reference in json file
    with open(high_score_fp, 'w') as f:
        json.dump({'high_score': score}, f)

def Your_score(score):
    value = font_style.render(str(score).zfill(4), True, black)
    dis.blit(value, [40, 10]) #location coordinates of score display

def create_rect(borderbuffer):
    x = borderbuffer
    y = borderbuffer
    width = dis_width - borderbuffer * 2
    height = dis_height - borderbuffer * 2
    pygame.draw.rect(dis, green, (x, y, width, height))
    pygame.draw.rect(dis, black, (x, y, width, height), 5)
    return x, y, width, height  

def display_game_over_message(high_score, current_score, old_high_score):
    lines = [
        "GAME OVER",
        f"SCORE: {current_score}",
        f"HIGH SCORE: {high_score}",
        "PRESS Q TO QUIT",
        "PRESS C TO PLAY AGAIN"
    ]

    if current_score == high_score and high_score > old_high_score:
        lines.append("A NEW HIGH SCORE!")  # Displays message if new high score obtained

    line_spacing = 5
    total_height = sum(font_style.render(line, True, black).get_height() for line in lines) + (line_spacing * (len(lines) - 1))
    start_y = (dis_height / 2) - (total_height / 2)

    for i, line in enumerate(lines):
        message = font_style.render(line, True, black)
        x_position = (dis_width - message.get_width()) / 2
        y_position = start_y + i * (message.get_height() + line_spacing)
        dis.blit(message, (x_position, y_position))

def snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

def generate_food(rect_x, rect_y, rect_width, rect_height):
    food_x = random.randrange(rect_x + snake_block, rect_x + rect_width - snake_block, snake_block)
    food_y = random.randrange(rect_y + snake_block, rect_y + rect_height - snake_block, snake_block)
    return food_x, food_y

def gameLoop():
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1
    old_high_score = load_high_score()
    high_score = load_high_score()

    rect_x, rect_y, rect_width, rect_height = create_rect(borderbuffer)
    foodx, foody = generate_food(rect_x, rect_y, rect_width, rect_height)

    pygame.display.set_caption("Snake")

    while not game_over:
        while game_close:
            current_score = length_of_snake - 1
            
            if current_score > high_score:
                save_high_score(current_score) #saves high score to json file
                high_score = current_score  # Updates high score for display

            dis.fill(green)
            create_rect(borderbuffer) #creates black border layout
            display_game_over_message(high_score, current_score, old_high_score)
            Your_score(current_score)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        # Updates position
        new_x1 = x1 + x1_change
        new_y1 = y1 + y1_change

        # checks to see if new position is within boundaries, triggers game over if not
        if rect_x <= new_x1 < rect_x + rect_width and rect_y <= new_y1 < rect_y + rect_height:
            x1 = new_x1
            y1 = new_y1
        else:
            game_close = True 

        dis.fill(green)
        create_rect(borderbuffer)
        pygame.draw.rect(dis, black, [foodx, foody, snake_block, snake_block])
        
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        #checks for collision with the food
        if snake_head[0] == foodx and snake_head[1] == foody:
            foodx, foody = generate_food(rect_x, rect_y, rect_width, rect_height)
            length_of_snake += 1
        else:
            for x in snake_list[:-1]:
                if x == snake_head:
                    game_close = True

        snake(snake_block, snake_list)
        Your_score(length_of_snake - 1)

        pygame.display.update()
        clock.tick(snake_speed)

    pygame.quit()
    quit()

if __name__ == "__main__":
    gameLoop()
