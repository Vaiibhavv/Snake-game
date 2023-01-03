import pygame as pg
import random
import os
#creating the head of snake.

pg.init()

## to adding the music module
pg.mixer.init()

white= (255,255,255)
black= (0,0,0)
red=  (255,0,0)
snake_width=900
snake_height=600

gamewindow= pg.display.set_mode((snake_width, snake_height))

## adding background images
bgimg= pg.image.load("home.jpg")
bgimg= pg.transform.scale(bgimg, (snake_width,snake_height)).convert_alpha()

pg.display.set_caption("First Game")   ## title of our game .
pg.display.update() 

## game specific variable
clock= pg.time.Clock()   ## for the velocity and fps
font= pg.font.SysFont(None,40,bold=30) ##  size and font of the score, on display

## creating the function which take the argument and display the score on window.

def text_screen(text, color, x ,y):  ## x= position of text in x direction and y direc.
    screen_text= font.render(text, True, color) ## for the color and and text
    gamewindow.blit(screen_text, [x,y])  ## for storing in memory location (logical)

def plot_rect(gamewindow, color,snk_list,snake_size):   ## creating the rectangle.
    for x ,y in snk_list:
        pg.draw.rect(gamewindow, color, [x,y, snake_size, snake_size])

## game loop 
def welcome():  # for  showing the home screen of the game . 
    exit_game=False
    while not exit_game:
        gamewindow.fill((230,220,210))
        gamewindow.blit(bgimg,(0,0))
        text_screen("PRESS ENTER TO CONTINUE",black, 240, 440)
        for event in pg.event.get():
            if event.type==pg.QUIT:
                exit_game=True
            
            if event.type==pg.KEYDOWN:   # if user press the enter  then game will be start.
                if event.key==pg.K_RETURN:
                    pg.mixer.music.load("back.mp3")
                    pg.mixer.music.play(-1)
                    gameloop()

        pg.display.update()
        clock.tick(60)    ## fps speed of the game 

def gameloop():
    exit_game= False
    game_over= False
    snake_x= 40
    snake_y=50
    snake_size=15
    fps= 30
    velocity_x= 0
    velocity_y=0
    init_velocity=5  ## velocity or speed of the snake when it wiill be moving.
    food_x=random.randint(0, snake_width) ## in x direction .
    food_y=random.randint(0, snake_height)   # position of x and y
    score=0 
    snk_lst=[]  ## to storing the all x and y position of snake 
    snake_len=1  ## initializing the length of the snake .
    ## checking whether file is exist or not

    if not os.path.exists("highscore.txt"):
        with open ("highscore.txt","w") as f:
            f.write("0")

    with open("highscore.txt","r") as f:
        highscore= f.read()              ## to creating the highscore file . 

    while not exit_game:
        if game_over:
            with open("highscore.txt","w") as f :  # if game over newhighscore will be stored in file .
                f. write(str(highscore))

            gamewindow.fill(white)   ##  the window will be fully white , 
            gamewindow.blit(bgimg,(0,0))
            text_screen("GAME OVER !! PRESS ENTER TO CONTINUE ",black,140,180)
            text_screen("SCORE : " +str(score) ,black, 300,440)
            text_screen("HIGHSCORE : " +str(highscore) ,black, 300,470)

            ## for cancel out the gamewindow
            for event in pg.event.get():
                if event.type==pg.QUIT:
                    exit_game=True
            ## to start new game . 
                if event.type==pg.KEYDOWN:
                    if event.key==pg.K_RETURN:   ## by pressing the enter key game will be restart
                        welcome()
        else:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit_game = True

                if event.type==pg.KEYDOWN:
                    if event.key==pg.K_RIGHT:
                        velocity_x=init_velocity  ## velocity in x direction will be increases by init_velocity
                        velocity_y=0

                    if event.key==pg.K_LEFT:
                        velocity_x=-init_velocity
                        velocity_y=0

                    if event.key==pg.K_UP:
                        velocity_y=-init_velocity
                        velocity_x=0
                    
                    if event.key==pg.K_DOWN:
                        velocity_y=init_velocity
                        velocity_x=0

                    if event.key==pg.K_q:
                        score+=10

            snake_x+=velocity_x       ## moving to straight by pressing the key.
            snake_y+=velocity_y

        ## if distance beetween x and y velocity is less than 6 then snake will eat to food.
            if abs(snake_x-food_x)<8 and abs(snake_y-food_y)<6:
                score+=10
                ## to create the food randomaly after eating by the snake.
                food_x=random.randint(20, snake_width/2) ## in x direction .
                food_y=random.randint(20, snake_height/2) 
                snake_len+=5  ## to if snake eat the food, then length of the snake will be increase by  5
                if score>int(highscore):  ## storing the new highscore vale
                    highscore= score

            gamewindow.fill(((154,205,50)))  ## we will get the white window
            text_screen("Score : " +str(score) ,black, 5,5)
            pg.draw.rect(gamewindow, red , [food_x, food_y, snake_size, snake_size])  ## creating the food for snake.

            head=[]
            head.append(snake_x)   ## snake starting position.
            head.append(snake_y)
            snk_lst.append(head)  ## and to putting in snk_list which taking the x, y 

            if len(snk_lst)>snake_len:  ## we are deleting the head of our snake, with every_i
                del snk_lst[0]
            
            if head in snk_lst[:-1]:  # if snake is crossing to itself. Then game will be end
                game_over=True
                pg.mixer.music.load("game_over.wav")
                pg.mixer.music.play()

            if snake_x<0 or snake_x>snake_width or snake_y<0 or snake_y>snake_height:
                game_over=True
                pg.mixer.music.load("game_over.wav")
                pg.mixer.music.play()
            #pg.draw.rect(gamewindow,black,[snake_x, snake_y, snake_size ,snake_size])
            plot_rect(gamewindow, black,snk_lst, snake_size)
        pg.display.update()    ## this function should be call when we made any update in our colours
        clock.tick(fps)  ## frame per second
    pg.quit()
    quit()
welcome()