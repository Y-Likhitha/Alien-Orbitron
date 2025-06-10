import pygame
import random
import math
from pygame import mixer
#intialize pygame
pygame.init()

#creating game window
width=750
height=500
window=pygame.display.set_mode((width,height))

#Adding title and icon
pygame.display.set_caption("Space Invaders")
icon=pygame.image.load('images/ufo.png')
pygame.display.set_icon(icon)

#adding background music
mixer.music.load('audio/backmusic.mp3')
mixer.music.play(-1)

#adding background image
background_img=pygame.image.load('images/back1.png')

#Adding spaceship image
space_image=pygame.image.load('images/space-invaders.png')
spaceX=320
spaceY=350
spaceX_change=0
spaceX_change=0

#Adding alien enemy image
enemy_img=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
no_of_enemies=6
for i in range(no_of_enemies):
    enemy_img.append(pygame.image.load('images/enemy.png'))
    enemyX.append(random.randint(0,686))
    enemyY.append(random.randint(70,210))
    enemyX_change.append(0.7)
    enemyY_change.append(20)

#Adding bullet image
# READY - we cannot fire bulllet
# FIRE - we can fire bullet
bullet_img=pygame.image.load('images/bullet.png')
bulletX=random.randint(0,750)
bulletY=random.randint(70,210)
bulletX_change=0
bulletY_change=3
bullet_state="ready"

# Printing score on window
score=0
score_font=pygame.font.Font('fonts/Pixelout Personal Use Only.ttf',32)
textX=300
textY=20

#game over text
game_over_font=pygame.font.Font('fonts/Pixelout Personal Use Only.ttf',70)

def game_over():
    game_over_text=game_over_font.render("Game Over ",True,(0,0,0))
    window.blit(game_over_text,(190,200))

def show_score(x,y):
    score_text=score_font.render("Score : "+str(score),True,(0,0,0))
    window.blit(score_text,(x,y))
#placing spaceship image on the window
def spaceship(x,y):
    window.blit(space_image,(x,y))

#placing enemy image on the window
def enemy(x,y,i):
    window.blit(enemy_img[i],(x,y))

#placing bullet image above spaceship
def fire_bullet(x,y):
    global bullet_state
    bullet_state="fire"
    window.blit(bullet_img,(x+16,y+20))

# collsion detection
def collision(enemyX,enemyY,bulletX,bulletY):
    distance=math.sqrt((math.pow(enemyX-bulletX,2))+(math.pow(enemyY-bulletY,2)))
    if distance<27:
        return True
    else:
        return False
   

#Basic Game Loop
run=True
while run:
    window.fill((255,255,255))
    #background image
    window.blit(background_img,(0,0))
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
        # moving spaceship to left or right
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_RIGHT:
                spaceX_change+=3
            if event.key==pygame.K_LEFT:
                spaceX_change-=3
            # firing bullet when spacebar is pressed
            if event.key==pygame.K_SPACE:
                if bullet_state is "ready":
                    #adding bullet sound
                    bullet_sound=mixer.Sound('audio/bullet.mp3')
                    bullet_sound.play()
                    bulletX=spaceX
                    fire_bullet(bulletX,bulletY)
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_RIGHT or event.key==pygame.K_LEFT:
                spaceX_change=0

            
    spaceX+=spaceX_change
    # making spaceship move within the window range
    if spaceX<=0:
        spaceX=0
    elif spaceX>=686:
        spaceX=686

    #making enemy move left to right and vice versa within the boundary
    for i in range(no_of_enemies):

        #displaying game over on window
        if enemyY[i]>310:
            for j in range(no_of_enemies):
                enemyY[i]=2000
            game_over()
            break
        enemyX[i]+=enemyX_change[i]
        if enemyX[i]<=0:
            enemyX[i]=0.1
            enemyY[i]+=enemyY_change[i]
        elif enemyX[i]>=686:
            enemyX[i]=-0.60
            enemyY[i]+=enemyY_change[i]
        collisions=collision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collisions:
            collision_sound=mixer.Sound('audio/collision.mp3')
            collision_sound.play()
            bulletY=370
            bullet_state="ready"
            score+=1
            enemyX[i]=random.randint(0,686)
            enemyY[i]=random.randint(70,210)
        enemy(enemyX[i],enemyY[i],i)



    # making bullet move upwards
    if bullet_state is "fire":
        fire_bullet(bulletX,bulletY)
        bulletY-=bulletY_change
    
    # firing mulitple bullets
    if bulletY<=0:
        bullet_state="ready"
        bulletY=370
    # if collision is detected and updating score
    
    spaceship(spaceX,spaceY)
    show_score(textX,textY)
    pygame.display.update()

