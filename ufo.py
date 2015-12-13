import pygame
import time
import random

pygame.init()

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('UFOs')

black = (0,0,0)
blue = (0,0,255)
red = (200,0,0)
light_red = (255,0,0)
yellow = (200,200,0)
light_yellow = (255,255,0)
green = (34,177,76)
light_green = (0,255,0)

purple = (100,0,100)
pink = (200,0,50)
light_purple = (150,20,70)

clock = pygame.time.Clock()

UFOWidth = 40
UFOHeight = 20
turretWidth = 5
wheelWidth = 5
ground_height = 35

smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 85)

def score(score):
    text = smallfont.render("Score: "+str(score), True, blue)
    gameDisplay.blit(text, [0,0])

def text_objects(text, color,size = "small"):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    if size == "medium":
        textSurface = medfont.render(text, True, color)
    if size == "large":
        textSurface = largefont.render(text, True, color)
    return textSurface, textSurface.get_rect()

def text_to_button(msg, color, buttonx, buttony, buttonwidth, buttonheight, size = "small"):
    textSurf, textRect = text_objects(msg,color,size)
    textRect.center = ((buttonx+(buttonwidth/2)), buttony+(buttonheight/2))
    gameDisplay.blit(textSurf, textRect)
   
def message_to_screen(msg,color, y_displace = 0, size = "small"):
    textSurf, textRect = text_objects(msg,color,size)
    textRect.center = (int(display_width / 2), int(display_height / 2)+y_displace)
    gameDisplay.blit(textSurf, textRect)

def UFO(x,y,turPos):
    x = int(x)
    y = int(y)

    possibleTurrets = [(x-27, y-2),
                       (x-26, y-5),
                       (x-25, y-8),
                       (x-23, y-12),
                       (x-20, y-14),
                       (x-18, y-15),
                       (x-15, y-17),
                       (x-13, y-19),
                       (x-11, y-21)
                       ]
  
    pygame.draw.circle(gameDisplay, purple, (x,y), int(UFOHeight/2))
    pygame.draw.ellipse(gameDisplay, purple, (x-UFOHeight, y, UFOWidth, UFOHeight))
    pygame.draw.line(gameDisplay, purple, (x,y), possibleTurrets[turPos], turretWidth)

    return possibleTurrets[turPos]

def enemy_UFO(x,y,turPos):
    x = int(x)
    y = int(y)

    possibleTurrets = [(x+27, y-2),
                       (x+26, y-5),
                       (x+25, y-8),
                       (x+23, y-12),
                       (x+20, y-14),
                       (x+18, y-15),
                       (x+15, y-17),
                       (x+13, y-19),
                       (x+11, y-21)
                       ]
  
    pygame.draw.circle(gameDisplay, pink, (x,y), int(UFOHeight/2))
    pygame.draw.ellipse(gameDisplay, pink, (x-UFOHeight, y, UFOWidth, UFOHeight))
    pygame.draw.line(gameDisplay, pink, (x,y), possibleTurrets[turPos], turretWidth)

    return possibleTurrets[turPos]

def game_controls():
    gcont = True

    while gcont:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

        gameDisplay.fill(black)
        message_to_screen("Controls",purple,-100,size="large")
        message_to_screen("Fire: Spacebar",blue,-30)
        message_to_screen("Move Turret: Up and Down arrows",blue,10)
        message_to_screen("Move UFO: Left and Right arrows",blue,50)
        message_to_screen("Pause: P",blue,90)


        button("play", 150,500,100,50, green, light_green, action="play")
        button("quit", 550,500,100,50, red, light_red, action ="quit")

        pygame.display.update()
        clock.tick(15)

def button(text, x, y, width, height, inactive_color, active_color, action = None):
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > cur[0] > x and y + height > cur[1] > y:
        pygame.draw.rect(gameDisplay, active_color, (x,y,width,height))
        if click[0] == 1 and action != None:
            if action == "quit":
                pygame.quit()
                quit()
            if action == "controls":
                game_controls()
            if action == "play":
                gameLoop()
            if action == "main":
                game_intro()
            
    else:
        pygame.draw.rect(gameDisplay, inactive_color, (x,y,width,height))

    text_to_button(text,black,x,y,width,height)

def pause():
    paused = True
    message_to_screen("Paused",purple,-100,size="large")
    message_to_screen("Press P to continue playing or Q to quit",blue,25)
    pygame.display.update()
    
    while paused:
        for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        quit()

        clock.tick(15)

def barrier(xlocation,randomHeight, barrier_width): 
    pygame.draw.rect(gameDisplay, blue, [xlocation, display_height-randomHeight, barrier_width,randomHeight])
    
def explosion(x, y, size=50):
    explode = True

    while explode:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        startPoint = x,y
        colorChoices = [purple, pink, light_purple, blue]
        magnitude = 1

        while magnitude < size:
            exploding_bit_x = x +random.randrange(-1*magnitude,magnitude)
            exploding_bit_y = y +random.randrange(-1*magnitude,magnitude)

            pygame.draw.circle(gameDisplay, colorChoices[random.randrange(0,4)], (exploding_bit_x,exploding_bit_y),random.randrange(1,5))
            magnitude += 1

            pygame.display.update()
            clock.tick(100)

        explode = False       

def fireShell(xy,UFOx,UFOy,turPos,gun_power,xlocation,barrier_width,randomHeight,enemyUFOX, enemyUFOY):
    fire = True
    damage = 0
    startingShell = list(xy)

    while fire:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.draw.circle(gameDisplay, red, (startingShell[0],startingShell[1]),5)

        startingShell[0] -= (12 - turPos)*2
        startingShell[1] += int((((startingShell[0]-xy[0])*0.015/(gun_power/50))**2) - (turPos+turPos/(12-turPos)))

        if startingShell[1] > display_height-ground_height:
            hit_x = int((startingShell[0]*display_height-ground_height)/startingShell[1])
            hit_y = int(display_height-ground_height)
            
            if enemyUFOX + 10 > hit_x > enemyUFOX - 10:
                damage = 25
            elif enemyUFOX + 15 > hit_x > enemyUFOX - 15:
                damage = 18
            elif enemyUFOX + 25 > hit_x > enemyUFOX - 25:
                damage = 10
            elif enemyUFOX + 35 > hit_x > enemyUFOX - 35:
                damage = 5          
            
            explosion(hit_x,hit_y)
            fire = False

        check_x_1 = startingShell[0] <= xlocation + barrier_width
        check_x_2 = startingShell[0] >= xlocation

        check_y_1 = startingShell[1] <= display_height
        check_y_2 = startingShell[1] >= display_height - randomHeight

        if check_x_1 and check_x_2 and check_y_1 and check_y_2:
            hit_x = int((startingShell[0]))
            hit_y = int(startingShell[1])
            explosion(hit_x,hit_y)
            fire = False           

        pygame.display.update()
        clock.tick(100)
    return damage
        
def e_fireShell(xy,UFOx,UFOy,turPos,gun_power,xlocation,barrier_width,randomHeight,pUFOx,pUFOy):
    damage = 0
    currentPower = 1
    power_found = False

    while not power_found:
        currentPower += 1
        if currentPower > 100:
            power_found = True

        fire = True
        startingShell = list(xy)

        while fire:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            startingShell[0] += (12 - turPos)*2
            startingShell[1] += int((((startingShell[0]-xy[0])*0.015/(currentPower/50))**2) - (turPos+turPos/(12-turPos)))

            if startingShell[1] > display_height-ground_height:
                hit_x = int((startingShell[0]*display_height-ground_height)/startingShell[1])
                hit_y = int(display_height-ground_height)
                if pUFOx+15 > hit_x > pUFOx - 15:
                    power_found = True
                fire = False

            check_x_1 = startingShell[0] <= xlocation + barrier_width
            check_x_2 = startingShell[0] >= xlocation

            check_y_1 = startingShell[1] <= display_height
            check_y_2 = startingShell[1] >= display_height - randomHeight

            if check_x_1 and check_x_2 and check_y_1 and check_y_2:
                hit_x = int((startingShell[0]))
                hit_y = int(startingShell[1])
                fire = False
    
    fire = True
    startingShell = list(xy)

    while fire:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.draw.circle(gameDisplay, red, (startingShell[0],startingShell[1]),5)

        startingShell[0] += (12 - turPos)*2

        gun_power = random.randrange(int(currentPower*0.90), int(currentPower*1.10))
        
        startingShell[1] += int((((startingShell[0]-xy[0])*0.015/(gun_power/50))**2) - (turPos+turPos/(12-turPos)))

        if startingShell[1] > display_height-ground_height:
            hit_x = int((startingShell[0]*display_height-ground_height)/startingShell[1])
            hit_y = int(display_height-ground_height)

            if pUFOx + 10 > hit_x > pUFOx - 10:
                print("Critical Hit!")
                damage = 25
            elif pUFOx + 15 > hit_x > pUFOx - 15:
                print("Hard Hit!")
                damage = 18
            elif pUFOx + 25 > hit_x > pUFOx - 25:
                print("Medium Hit")
                damage = 10
            elif pUFOx + 35 > hit_x > pUFOx - 35:
                print("Light Hit")
                damage = 5
            
            explosion(hit_x,hit_y)
            fire = False

        check_x_1 = startingShell[0] <= xlocation + barrier_width
        check_x_2 = startingShell[0] >= xlocation

        check_y_1 = startingShell[1] <= display_height
        check_y_2 = startingShell[1] >= display_height - randomHeight

        if check_x_1 and check_x_2 and check_y_1 and check_y_2:
            hit_x = int((startingShell[0]))
            hit_y = int(startingShell[1])
            explosion(hit_x,hit_y)
            fire = False   

        pygame.display.update()
        clock.tick(100)
    return damage

def power(level):
    text = smallfont.render("Power: "+str(level)+"%",True, blue)
    gameDisplay.blit(text, [display_width/2,0])

def game_intro():

    intro = True

    while intro:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        intro = False
                    elif event.key == pygame.K_q:                        
                        pygame.quit()
                        quit()

        gameDisplay.fill(black)
        message_to_screen("Welcome to UFOs!",purple,-100,size="large")
        message_to_screen("The objective is to shoot and destroy",blue,-30)
        message_to_screen("the enemy UFO before they destroy you.",blue,10)

        button("play", 150,500,100,50, green, light_green, action="play")
        button("controls", 350,500,100,50, yellow, light_yellow, action="controls")
        button("quit", 550,500,100,50, red, light_red, action ="quit")

        pygame.display.update()
        clock.tick(15)

def game_over():
    game_over = True

    while game_over:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

        gameDisplay.fill(black)
        message_to_screen("Game Over",purple,-100,size="large")
        message_to_screen("You died.",blue,-30)

        button("play Again", 150,500,150,50, green, light_green, action="play")
        button("controls", 350,500,100,50, yellow, light_yellow, action="controls")
        button("quit", 550,500,100,50, red, light_red, action ="quit")

        pygame.display.update()
        clock.tick(15)

def you_win():
    win = True

    while win:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

        gameDisplay.fill(black)
        message_to_screen("You won!",purple,-100,size="large")
        message_to_screen("Congratulations!",blue,-30)

        button("play Again", 150,500,150,50, green, light_green, action="play")
        button("controls", 350,500,100,50, yellow, light_yellow, action="controls")
        button("quit", 550,500,100,50, red, light_red, action ="quit")

        pygame.display.update()
        clock.tick(15)

def health_bars(player_health, enemy_health):
    if player_health > 75:
        player_health_color = green
    elif player_health > 50:
        player_health_color = yellow
    else:
        player_health_color = red

    if enemy_health > 75:
        enemy_health_color = green
    elif enemy_health > 50:
        enemy_health_color = yellow
    else:
        enemy_health_color = red

    pygame.draw.rect(gameDisplay, player_health_color, (680, 25, player_health, 25))
    pygame.draw.rect(gameDisplay, enemy_health_color, (20, 25, enemy_health, 25))

def gameLoop():
    gameExit = False
    gameOver = False
    FPS = 15

    player_health = 100
    enemy_health = 100

    barrier_width = 50

    mainUFOX = display_width * 0.9
    mainUFOY = display_height * 0.9
    UFOMove = 0
    currentTurPos = 0
    changeTur = 0

    enemyUFOX = display_width * 0.1
    enemyUFOY = display_height * 0.9 

    fire_power = 50
    power_change = 0

    xlocation = (display_width/2) + random.randint(-0.1*display_width, 0.1*display_width) 
    randomHeight = random.randrange(display_height*0.1,display_height*0.6)
  
    while not gameExit:     
        if gameOver == True:
            message_to_screen("Game Over",red,-50,size="large")
            message_to_screen("Press C to play again or Q to exit",blue,50)
            pygame.display.update()
            while gameOver == True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameExit = True
                        gameOver = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_c:
                            gameLoop()
                        elif event.key == pygame.K_q:
                            gameExit = True
                            gameOver = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                      UFOMove = -5                
                elif event.key == pygame.K_RIGHT:
                    UFOMove = 5       
                elif event.key == pygame.K_UP:
                    changeTur = 1  
                elif event.key == pygame.K_DOWN:
                    changeTur = -1
                elif event.key == pygame.K_p:
                    pause()
                elif event.key == pygame.K_SPACE:                    
                    damage = fireShell(gun,mainUFOX,mainUFOY,currentTurPos,fire_power,xlocation,barrier_width,randomHeight,enemyUFOX,enemyUFOY)
                    enemy_health -= damage

                    possibleMovement = ['f','r']
                    moveIndex = random.randrange(0,2)

                    for x in range(random.randrange(0,10)):
                        if display_width * 0.3 > enemyUFOX > display_width * 0.03:
                            if possibleMovement[moveIndex] == "f":
                                enemyUFOX += 5
                            elif possibleMovement[moveIndex] == "r":
                                enemyUFOX -= 5

                            gameDisplay.fill(black)
                            health_bars(player_health,enemy_health)
                            gun = UFO(mainUFOX,mainUFOY,currentTurPos)
                            enemy_gun = enemy_UFO(enemyUFOX, enemyUFOY, 8)
                            fire_power += power_change
                            power(fire_power)
                            barrier(xlocation,randomHeight,barrier_width)
                            gameDisplay.fill(blue, rect=[0, display_height-ground_height, display_width, ground_height])

                            pygame.display.update()
                            clock.tick(FPS)
                    
                    damage = e_fireShell(enemy_gun,enemyUFOX,enemyUFOY,8,50,xlocation,barrier_width,randomHeight,mainUFOX,mainUFOY)
                    player_health -= damage
                    
                elif event.key == pygame.K_a:
                    power_change = -1
                elif event.key == pygame.K_d:
                    power_change = 1

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    UFOMove = 0

                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    changeTur = 0
                    
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    power_change = 0
        
        mainUFOX += UFOMove
        currentTurPos += changeTur

        if currentTurPos > 8:
            currentTurPos = 8
        elif currentTurPos < 0:
            currentTurPos = 0

        if mainUFOX - (UFOWidth/2) < xlocation+barrier_width:
            mainUFOX += 5            

        gameDisplay.fill(black)
        health_bars(player_health,enemy_health)
        gun = UFO(mainUFOX,mainUFOY,currentTurPos)
        enemy_gun = enemy_UFO(enemyUFOX, enemyUFOY, 8)        
        fire_power += power_change

        if fire_power > 100:
            fire_power = 100
        elif fire_power < 1:
            fire_power = 1   

        power(fire_power)
        barrier(xlocation,randomHeight,barrier_width)
        gameDisplay.fill(blue, rect=[0, display_height-ground_height, display_width, ground_height])
        pygame.display.update()

        if player_health < 1:
            game_over()
        elif enemy_health < 1:
            you_win()
        clock.tick(FPS)

    pygame.quit()
    quit()
    
game_intro()
gameLoop()
