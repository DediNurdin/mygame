import pygame
import math
from pygame.locals import *
from random import randint


pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))

keys = {
    "top": False,
    "bottom": False,
    "left": False,
    "right": False
}

running = True

playerpos = [100, 100] 

exitcode = 0
EXIT_CODE_GAME_OVER = 0
EXIT_CODE_WIN = 1
score = 0
health_point = 194
countdown_timer = 90000
arrows = []

enemy_timer = 100
enemies = [[width, 100]]

player = pygame.image.load("resources/images/dude.png")
grass = pygame.image.load("resources/images/grass.png")
castle = pygame.image.load("resources/images/castle.png")
arrow = pygame.image.load("resources/images/bullet.png")
enemy_img = pygame.image.load("resources/images/badguy.png")
healthbar = pygame.image.load("resources/images/healthbar.png")
health = pygame.image.load("resources/images/health.png")
gameover = pygame.image.load("resources/images/gameover.png")
youwin = pygame.image.load("resources/images/youwin.png")


pygame.mixer.init()
hit_sound = pygame.mixer.Sound("resources/audio/explode.wav")
enemy_hit_sound = pygame.mixer.Sound("resources/audio/enemy.wav")
shoot_sound = pygame.mixer.Sound("resources/audio/shoot.wav")
hit_sound.set_volume(0.05)
enemy_hit_sound.set_volume(0.05)
shoot_sound.set_volume(0.05)

pygame.mixer.music.load("resources/audio/moonlight.wav")
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)

while(running):
    
    screen.fill(0)
    
    for x in range(int(width/grass.get_width()+1)):
        for y in range(int(height/grass.get_height()+1)):
            screen.blit(grass, (x*100, y*100))

    screen.blit(castle, (1, 30))
    screen.blit(castle, (0, 135))
    screen.blit(castle, (0, 240))
    screen.blit(castle, (0, 345))
    
    mouse_position = pygame.mouse.get_pos()
    angle = math.atan2(mouse_position[1] - (playerpos[1]+32), mouse_position[0] - (playerpos[0]+26))
    player_rotation = pygame.transform.rotate(player, 360 - angle * 57.29)
    new_playespos = (playerpos[0] - player_rotation.get_rect().width / 2, playerpos[1] - player_rotation.get_rect().height / 2)
    screen.blit(player_rotation, new_playespos)
    
    for bullet in arrows:
        arrow_index = 0
        velx=math.cos(bullet[0])*10
        vely=math.sin(bullet[0])*10
        bullet[1]+=velx
        bullet[2]+=vely
        if bullet[1] < -64 or bullet[1] > width or bullet[2] < -64 or bullet[2] > height:
            arrows.pop(arrow_index)
        arrow_index += 1

        for projectile in arrows:
            new_arrow = pygame.transform.rotate(arrow, 360-projectile[0]*57.29)
            screen.blit(new_arrow, (projectile[1], projectile[2]))

    enemy_timer -= 1
    if enemy_timer == 0:
        enemies.append([width, randint(50, height-32)])
        enemy_timer = randint(1, 100)

    index = 0
    for enemy in enemies:
        enemy[0] -= 5

        if enemy[0] < -64:
            enemies.pop(index)

        enemy_rect = pygame.Rect(enemy_img.get_rect())
        enemy_rect.top = enemy[1]
        enemy_rect.left = enemy[0]

        if enemy_rect.left < 64:
            enemies.pop(index)
            health_point -= randint(5,20)
            hit_sound.play()
            print("Watch out! we are attacked!!")

        index_arrow = 0
        for bullet in arrows:
            bullet_rect = pygame.Rect(arrow.get_rect())
            bullet_rect.left = bullet[1]
            bullet_rect.top = bullet[2]

            if enemy_rect.colliderect(bullet_rect):
                score += 1
                enemies.pop(index)
                arrows.pop(index_arrow)
                enemy_hit_sound.play()
                print("Boom!, die you damn! ")
                print("Score: {}".format(score))
            index_arrow =+ 1
        index += 1

    for enemy in enemies:
        screen.blit(enemy_img, enemy)

    screen.blit(healthbar, (5,5))
    for hp in range(health_point):
        screen.blit(health, (hp+8, 8))

    font = pygame.font.Font(None, 24)
    minutes = int((countdown_timer-pygame.time.get_ticks())/60000)
    seconds = int((countdown_timer-pygame.time.get_ticks())/1000%60)
    time_text = "{:022}:{:02}".format(minutes, seconds)
    clock = font.render(time_text, True, (255,255,255))
    textRect = clock.get_rect()
    textRect.topright = [635, 5]
    screen.blit(clock, textRect)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

        if event.type == pygame.MOUSEBUTTONDOWN:
            arrows.append([angle, new_playespos[0]+32, new_playespos[1]+32])
            shoot_sound.play()

        if event.type == pygame.KEYDOWN:
            if event.key == K_w:
                keys["top"] = True
            elif event.key == K_a:
                keys["left"] = True
            elif event.key == K_s:
                keys["bottom"] = True
            elif event.key == K_d:
                keys["right"] = True
        if event.type == pygame.KEYUP:
            if event.key == K_w:
                keys["top"] = False
            elif event.key == K_a:
                keys["left"] = False
            elif event.key == K_s:
                keys["bottom"] = False
            elif event.key == K_d:
                keys["right"] = False

    if keys["top"]:
        playerpos[1] -= 5
    elif keys["bottom"]:
        playerpos[1] += 5
    if keys["left"]:
        playerpos[0] -= 5
    elif keys["right"]:
        playerpos[0] += 5 

    if pygame.time.get_ticks() > countdown_timer:
        running = False
        exitcode = EXIT_CODE_WIN
    if health_point <= 0:
        running = False
        exitcode = EXIT_CODE_GAME_OVER


if exitcode == EXIT_CODE_GAME_OVER:
    screen.blit(gameover, (0, 0))
else:
    screen.blit(youwin, (0, 0))

text = font.render("Score: {}".format(score), True, (255, 255, 255))
textRect = text.get_rect()
textRect.centerx = screen.get_rect().centerx
textRect.centery = screen.get_rect().centery + 24
screen.blit(text, textRect)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    pygame.display.flip()