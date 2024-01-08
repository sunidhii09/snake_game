import pygame
import time
import random

pygame.init()
pygame.mixer.init()
 
yellow= (255, 255, 0)
green=(0, 255, 0)
red= (255, 0, 0)
 
dis_width= 1200
dis_height= 600

dis= pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()
snake_block= 10
snake_speed= 15

font_style = pygame.font.SysFont("comicsansms", 30)
score_font = pygame.font.SysFont("bahnschrift", 30)

pygame.mixer.music.load("./Snake Game - Theme Song.mp3")
pygame.mixer.music.play(-1)

eating_sound = pygame.mixer.Sound("./rattles-80176.mp3")
game_over_sound = pygame.mixer.Sound("./negative_beeps-6008.mp3")

def score(s):
    val=score_font.render("Your Score: " + str(s), True, red)
    dis.blit(val, [0,0])

def snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, green, [x[0], x[1], snake_block, snake_block])

# def message(msg, color):
#     mesg = font_style.render(msg, True, color)
#     dis.blit(mesg, [dis_width/8, dis_height/2])

def gameLoop():
    game_over=False
    game_close=False
    food, sound=False, False

    x1= dis_width/2
    y1= dis_height/2

    x1_change= 0
    y1_change= 0

    snake_list=[]
    l=1

    food_x= round(random.randrange(0, dis_width-snake_block)/10.0)*10.0
    food_y= round(random.randrange(0, dis_height-snake_block)/10.0)*10.0

    while not game_over:
        while game_close==True:
            dis.fill(yellow)
            play_again_msg = font_style.render("Game over! Press Q to Exit or C to Play Again.", True, red)
            pygame.mixer.music.stop()
            if not sound:
                game_over_sound.play()
                sound=True

            dis.blit(play_again_msg, [dis_width/6, dis_height/2 - play_again_msg.get_height()/2])
            pygame.display.update()

            for event in pygame.event.get():
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_q:
                        game_over=True
                        game_close=False
                    if event.key==pygame.K_c:
                        pygame.mixer.music.play(-1)
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

        # if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
        #     game_over = True

        x1 += x1_change
        y1 += y1_change
        dis.fill(yellow)
        pygame.draw.circle(dis, red, (food_x + snake_block // 2, food_y + snake_block // 2), snake_block // 2)
        snake_head=[]
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)

        if len(snake_list) > l:
            del snake_list[0]
        
        for x in snake_list[:-1]:
            if x==snake_head:
                game_close=True

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            pygame.mixer.music.stop()
            game_over = True
            game_over_sound.play()

        snake(snake_block, snake_list)
        score(l-1)
        pygame.display.update()

        if x1 == food_x and y1 == food_y:
            if not food:
                eating_sound.play()
                food=True

            pygame.time.delay(300)
            food_x = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            food_y = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

            while [food_x, food_y] in snake_list:
                food_x = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
                food_y = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

            l+=1
            food=False

        clock.tick(snake_speed)

    pygame.mixer.music.stop()
    game_over_sound.play()
    lost_msg = font_style.render("You Lost!", True, red)
    dis.blit(lost_msg, [(dis_width - lost_msg.get_width()) / 2, (dis_height - lost_msg.get_height()) / 2])

    pygame.display.update()
    time.sleep(2)
    pygame.quit()

    quit()

gameLoop()
