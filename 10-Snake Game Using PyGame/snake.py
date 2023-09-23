# our game imports
import pygame, sys, random, time, os

# check for initializing errors
check_errors = pygame.init()
if check_errors[1] > 0:
    print("(!) Had {0} initializing errors, exiting...".format(check_errors[1]))
    sys.exit(-1)
else:
    print("(+) PyGame successfully initialized!")

# Play surface
main_canvas = pygame.display.set_mode((720, 460))
pygame.display.set_caption('Python Snake game!')

# Colors
red   = pygame.Color(255, 0, 0) # gameover text color
green = pygame.Color(0, 255, 0) #snake body color
black = pygame.Color(0, 0, 0) #score card color
white = pygame.Color(255, 255, 255) #background color
brown = pygame.Color(165, 42, 42) #food color

# FPS controller
fpsController = pygame.time.Clock()

# Define the high scores file
high_scores_file = "./snake/high_scores.txt"
high_scores = []
# Important varibles
snake_position = [100, 50]
snake_body = [[100,50], [90,50], [80,50]]

food_position = [random.randrange(1,144)*5,random.randrange(1,92)*5]
food_spawn = True

direction = 'RIGHT'
changeto = direction

score = 0


# Game over function
def gameOver(current_score, high_scores_file):

    high_scores = updateHighScores(current_score, high_scores_file)

    myFont = pygame.font.SysFont('monaco', 72)
    GOsurf = myFont.render('Game over!', True, red)
    GOrect = GOsurf.get_rect()
    GOrect.midtop = (360, 15)
    main_canvas.blit(GOsurf,GOrect)
    showScore(current_score, high_scores)
    pygame.display.flip()
    
    time.sleep(5)

    pygame.quit() #pygame exit
    sys.exit() #console exit

# Display Current Score as well as top 5 highest scores
def showScore(current_score, high_scores):
    sFont = pygame.font.SysFont('monaco', 24)
    Ssurf = sFont.render('Score : {0}'.format(current_score), True, white)
    Srect = Ssurf.get_rect()
    Srect.midtop = (80, 10)
    main_canvas.blit(Ssurf, Srect)

    hFont = pygame.font.SysFont('monaco', 24)
    for i, score in enumerate(high_scores):
        hSurf = hFont.render('High Score {0}: {1}'.format(i + 1, score), True, white)
        hRect = hSurf.get_rect()
        hRect.midtop = (360, 150 + i * 30)
        main_canvas.blit(hSurf, hRect)

# Top five highest scores
def updateHighScores(current_score, high_scores_file):
    # Create the high scores file if it does not exist
    if not os.path.exists(high_scores_file):
        with open(high_scores_file, 'w') as file:
            file.write('0\n' * 5)  # Initialize with 5 zeros

    with open(high_scores_file, 'r') as file:
        high_scores = [int(line.strip()) for line in file]

    high_scores.append(current_score)
    high_scores.sort(reverse=True)
    high_scores = high_scores[:5]

    # with open(high_scores_file, 'w') as file:
    #     for score in high_scores:
    #         file.write(str(score) + '\n')

    return high_scores


# Main Logic of the game
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                changeto = 'RIGHT' 
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                changeto = 'LEFT' 
            if event.key == pygame.K_UP or event.key == ord('w'):
                changeto = 'UP' 
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                changeto = 'DOWN' 
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    # validation of direction
    if changeto == 'RIGHT' and not direction == 'LEFT':
        direction = 'RIGHT'
    if changeto == 'LEFT' and not direction == 'RIGHT':
        direction = 'LEFT'
    if changeto == 'UP' and not direction == 'DOWN':
        direction = 'UP'
    if changeto == 'DOWN' and not direction == 'UP':
        direction = 'DOWN'

    # Update snake position [x,y]
    if direction == 'RIGHT':
        snake_position[0] += 5
    if direction == 'LEFT':
        snake_position[0] -= 5
    if direction == 'UP':
        snake_position[1] -= 5
    if direction == 'DOWN':
        snake_position[1] += 5
    
    
    # Snake body mechanism
    snake_body.insert(0, list(snake_position))
    if snake_position[0] == food_position[0] and snake_position[1] == food_position[1]:
        score += 1
        food_spawn = False
    else:
        snake_body.pop()
        
    #Food Spawn
    if food_spawn == False:
        food_position = [random.randrange(1,144)*5,random.randrange(1,92)*5]
    food_spawn = True
    
    #Background
    main_canvas.fill(black)
    
    #Draw Snake 
    for pos in snake_body:
        pygame.draw.rect(main_canvas, green, pygame.Rect(pos[0],pos[1],5,5))
    
    pygame.draw.rect(main_canvas, white, pygame.Rect(food_position[0],food_position[1],5,5))
    
    # Bound
    if snake_position[0] > 715 or snake_position[0] < 0:
        high_scores = updateHighScores(score, high_scores_file)
        gameOver(score, high_scores_file)
    if snake_position[1] > 455 or snake_position[1] < 0:
        high_scores = updateHighScores(score, high_scores_file)
        gameOver(score, high_scores_file)
        
    # Self hit
    for block in snake_body[1:]: 
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            gameOver(score, high_scores_file)

    
    #common stuff
    showScore(score, high_scores)
    pygame.display.flip()
    
    fpsController.tick(20)