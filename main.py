import pygame
import random

from pygame import mixer

#Initialize pygame
pygame.init()

#Create the screen
screenWidth = 800
screenHeight = 600
screen = pygame.display.set_mode((screenWidth,screenHeight))

#Background
background = pygame.image.load('Space background.jpg')
background = pygame.transform.scale(background,(screenWidth, screenHeight))

#Background Sound
mixer.music.load("background.wav")
mixer.music.play(-1)
mixer.music.set_volume(0.1)

#Effect sound
bullet_sound = mixer.Sound('laser.wav')
bullet_sound.set_volume(0.1)
explosion_sound = mixer.Sound('explosion.wav')
explosion_sound.set_volume(0.1)



#Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('SpaceInvaderLogo.png')
pygame.display.set_icon(icon)

#Player
spaceshipSize = 64 #64 pixels
playerImg = pygame.image.load('spaceship.png')
playerX = 370   #top left == (0,0)
playerY = 480
playerX_change = 0
#playerY_change = 0

#Bullet
bulletSize = 32
bulletImg = pygame.image.load('bullet.png')
bulletX = 0   #choose random number for location of enemy
bulletY = playerY
bulletX_change = 0
bulletY_change = 1
bullet_state = "ready"
#Ready - bullet not shown on screen
#Fire - bullet is moving on screen

#Score
score_value = 0
font = pygame.font.Font("freesansbold.ttf",32)
textX = 10
textY = 10

over_font = pygame.font.Font("freesansbold.ttf",64)


#Enemy
enemySize = []
enemyImg = []
enemyX = []   #choose random number for location of enemy
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemySize.append(64) #64 pixels
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0,screenWidth - enemySize[i]))   #choose random number for location of enemy
    enemyY.append(random.randint(50,150))
    enemyX_change.append(0.3)
    enemyY_change.append(40)




#Function to draw the player
def player(x,y):
    screen.blit(playerImg,(x,y))

def enemy(x,y,i):
    screen.blit(enemyImg[i], (x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(x + 16,y + 10))

def show_score(x,y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score,(x,y))

def isCollision(i,enemyX,enemyY,enemySize,bulletX,bulletY,bulletSize):
    enemyRect = pygame.Rect(enemyX[i],enemyY[i],enemySize[i],enemySize[i])
    bulletRect = pygame.Rect(bulletX,bulletY,bulletSize,bulletSize)
    return enemyRect.colliderect(bulletRect)

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200,250))

#Game loop
running = True
while running:    
    #Fill RGB code for the color of a screen (0-255)
    screen.fill((0,0,0))

    #Load background
    screen.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #Check if key is pressed
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
            elif event.key == pygame.K_RIGHT:
                playerX_change = 0.3
            elif event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletX = playerX
                    fire_bullet(bulletX,bulletY)
                    bullet_sound.play()

        #Check if key is released
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0        


    #Draw player on the screen
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= screenWidth - spaceshipSize:
        playerX = screenWidth - spaceshipSize

    #Enemy movement
    for i in range(num_of_enemies):
        
        #Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break


        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= screenWidth - enemySize[i]:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]

        #Collision
        if isCollision(i,enemyX,enemyY,enemySize,bulletX,bulletY,bulletSize):
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            #Spawning new enemy
            enemyX[i] = random.randint(0,screenWidth - enemySize[i]) 
            enemyY[i] = random.randint(50,150)
        
        enemy(enemyX[i],enemyY[i],i)

    #Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change


    player(playerX,playerY)
    show_score(textX,textY)
    pygame.display.update()

