import pygame
import random
import math

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500

PLAYER_START_X = 370
PLAYER_START_Y = 380
PLAYER_SPEED = 5

ENEMY_START_Y_MIN = 50
ENEMY_START_Y_MAX = 150
ENEMY_SPEED_X = 3
NUM_ENEMIES = 7
COLLISION_DISTANCE = 30

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Player & Enemies")

background = pygame.image.load("background.png")
playerImg = pygame.image.load("player.png")
enemyImg = pygame.image.load("enemy.png")

playerX = PLAYER_START_X
playerY = PLAYER_START_Y
playerX_change = 0
playerY_change = 0

enemies = []
for _ in range(NUM_ENEMIES):
    enemyX = random.randint(0, SCREEN_WIDTH - 64)
    enemyY = random.randint(ENEMY_START_Y_MIN, ENEMY_START_Y_MAX)
    enemyX_change = random.choice([-ENEMY_SPEED_X, ENEMY_SPEED_X])
    enemies.append([enemyX, enemyY, enemyX_change])

score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textX, textY = 10, 10

over_font = pygame.font.Font("freesansbold.ttf", 64)


def show_score(x, y):
    score = font.render(f"Score: {score_value}", True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y):
    screen.blit(enemyImg, (x, y))


def is_collision(x1, y1, x2, y2):
    distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    return distance < COLLISION_DISTANCE


running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -PLAYER_SPEED
            if event.key == pygame.K_RIGHT:
                playerX_change = PLAYER_SPEED
            if event.key == pygame.K_UP:
                playerY_change = -PLAYER_SPEED
            if event.key == pygame.K_DOWN:
                playerY_change = PLAYER_SPEED

        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                playerX_change = 0
            if event.key in [pygame.K_UP, pygame.K_DOWN]:
                playerY_change = 0

    playerX += playerX_change
    playerY += playerY_change
    playerX = max(0, min(playerX, SCREEN_WIDTH - 64))
    playerY = max(0, min(playerY, SCREEN_HEIGHT - 64))

    for i in range(NUM_ENEMIES):
        enemies[i][0] += enemies[i][2]
        if enemies[i][0] <= 0 or enemies[i][0] >= SCREEN_WIDTH - 64:
            enemies[i][2] *= -1
            enemies[i][1] += 40

        if is_collision(playerX, playerY, enemies[i][0], enemies[i][1]):
            score_value += 1
            enemies[i][0] = random.randint(0, SCREEN_WIDTH - 64)
            enemies[i][1] = random.randint(ENEMY_START_Y_MIN, ENEMY_START_Y_MAX)

        enemy(enemies[i][0], enemies[i][1])

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
