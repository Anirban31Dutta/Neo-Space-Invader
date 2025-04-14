import pygame
import math
import random
import sys

from pygame import mixer

# Initialize pygame
pygame.init()

# Create the screen
WIDTH = 800
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))

# Background
background = pygame.image.load('Image/background.jpeg')

# Background sound
mixer.music.load('Sound/background.wav')
mixer.music.play(-1)

# Colours
WHITE = (255, 255, 255)

# Player
playerImg = pygame.image.load('Image/space-invaders.png')
player_rect = playerImg.get_rect()
player_rect.x = WIDTH // 2 - player_rect.width // 2
player_rect.y = HEIGHT - player_rect.height - 10


# Enemy spaceship
enemyImg = pygame.image.load("Image/alien.png")
enemy_rect = enemyImg.get_rect()
enemy_spacing = 10

# Create the enemy grid
enemies = []
num_rows = 3
num_cols = 10
for row in range(num_rows):
    for col in range(num_cols):
        enemy = enemy_rect.copy()
        enemy.x = 50 + col * (enemy_rect.width + enemy_spacing)
        enemy.y = 50 + row * (enemy_rect.height + enemy_spacing)
        enemies.append(enemy)

# Bullet
# Ready- You can't see the bullet on the screen
# Fire- The bullet is currently moving
bulletImg = pygame.image.load('Image/bullet.png')
bullet_rect = bulletImg.get_rect()
bullets = []
bullet_state = "ready"

enemy_bulletImg = pygame.image.load('Image/enemy_bullet.png')
enemy_bullet_rect = enemy_bulletImg.get_rect()
enemy_bullets = []


# Game variables
running = True
clock = pygame.time.Clock()
level = 1
score = 0

# Level-specific settings
bullet_cooldown = 500 - (level * 50)  # Decrease bullet cooldown with each level
enemy_bullet_cooldown = 500 - (level * 50)  # Decrease enemy bullet cooldown with each level

# Initialize bullet times
last_bullet_time = pygame.time.get_ticks() - bullet_cooldown
last_enemy_bullet_time = pygame.time.get_ticks() - enemy_bullet_cooldown


# Game states
game_active = False
mute_music = False
points = 0
ship_purchased = False



def show_menu():
    global game_active
    global mute_music
    global points
    global ship_purchased
    menu_font = pygame.font.Font(None, 50)
    title_font = pygame.font.Font(None, 80)

    while not game_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        window.blit(background, (0, 0))
        title_text = title_font.render("Space Invaders", True, WHITE)
        start_text = menu_font.render("Start Game", True, WHITE)
        option_text = menu_font.render("Options", True, WHITE)
        quit_text = menu_font.render("Quit", True, WHITE)

        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
        start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        option_rect = option_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        quit_rect = quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))

        window.blit(title_text, title_rect)
        window.blit(start_text, start_rect)
        window.blit(option_text, option_rect)
        window.blit(quit_text, quit_rect)

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        if start_rect.collidepoint(mouse_pos) and mouse_pressed[0]:
            game_active = True
        elif option_rect.collidepoint(mouse_pos) and mouse_pressed[0]:
            show_options()
        elif quit_rect.collidepoint(mouse_pos) and mouse_pressed[0]:
            pygame.quit()
            sys.exit()

        pygame.display.update()

def show_options():
    global mute_music
    global points
    global ship_purchased
    options_active = True
    menu_font = pygame.font.Font(None, 50)

    while options_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        window.blit(background, (0, 0))
        title_text = menu_font.render("Options", True, WHITE)
        mute_text = menu_font.render("Mute Music: " + ("On" if mute_music else "Off"), True, WHITE)
        buy_text = menu_font.render("Buy Ship (Cost: 100 Points)", True, WHITE)
        points_text = menu_font.render("Points: " + str(points), True, WHITE)
        back_text = menu_font.render("Back", True, WHITE)

        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 150))
        mute_rect = mute_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        buy_rect = buy_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        points_rect = points_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 150))
        back_rect = back_text.get_rect(center=(WIDTH // 2, HEIGHT - 100))

        window.blit(title_text, title_rect)
        window.blit(mute_text, mute_rect)
        window.blit(buy_text, buy_rect)
        window.blit(points_text, points_rect)
        window.blit(back_text, back_rect)

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        if mute_rect.collidepoint(mouse_pos) and mouse_pressed[0]:
            mute_music = not mute_music
        elif buy_rect.collidepoint(mouse_pos) and mouse_pressed[0]:
            if points >= 100 and not ship_purchased:
                ship_purchased = True
                points -= 100
        elif back_rect.collidepoint(mouse_pos) and mouse_pressed[0]:
            options_active = False

        pygame.display.update()

show_menu()

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('Image/space-invaders.png' )
pygame.display.set_icon(icon)

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()

    keys = pygame.key.get_pressed()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and player_rect.x > 0:
        player_rect.x -= 5
    if keys[pygame.K_RIGHT] and player_rect.x < WIDTH - player_rect.width:
        player_rect.x += 5

    if keys[pygame.K_SPACE]:
        if bullet_state == "ready":
            bullet_Sound = mixer.Sound('Sound/laser.wav')
            bullet_Sound.play()

        current_time = pygame.time.get_ticks()
        if current_time - last_bullet_time >= bullet_cooldown:
            bullet = bullet_rect.copy()
            bullet.x = player_rect.x + player_rect.width // 2 - bullet_rect.width // 2
            bullet.y = player_rect.y - bullet_rect.height
            bullets.append(bullet)
            last_bullet_time = current_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and player_rect.x > 0:
        player_rect.x -= 5
    if keys[pygame.K_RIGHT] and player_rect.x < WIDTH - player_rect.width:
        player_rect.x += 5

    if keys[pygame.K_SPACE]:
        if bullet_state == "ready":
            bullet_Sound = mixer.Sound('Sound/laser.wav')
            bullet_Sound.play()

        current_time = pygame.time.get_ticks()
        if current_time - last_bullet_time >= bullet_cooldown:
            bullet = bullet_rect.copy()
            bullet.x = player_rect.x + player_rect.width // 2 - bullet_rect.width // 2
            bullet.y = player_rect.y - bullet_rect.height
            bullets.append(bullet)
            last_bullet_time = current_time

    if len(enemy_bullets) < 5:
        current_time = pygame.time.get_ticks()
        if (current_time - last_enemy_bullet_time >= enemy_bullet_cooldown):
            enemy = random.choice(enemies)
            enemy_bullet = enemy_bullet_rect.copy()
            enemy_bullet.x = enemy.x + enemy.width // 2 - enemy_bullet_rect.width // 2
            enemy_bullet.y = enemy.y + enemy.height
            enemy_bullets.append(enemy_bullet)
            last_enemy_bullet_time = current_time

    for bullet in bullets:
        bullet.y -= 5
        if bullet.y < 0:
            bullets.remove(bullet)
        else:
            for enemy in enemies:
                if bullet.colliderect(enemy):
                    explosion_Sound = mixer.Sound('Sound/explosion.wav')
                    explosion_Sound.play()
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 10  # Increase the score for  each enemy hit

    for enemy_bullet in enemy_bullets:
        enemy_bullet.y += 5
        if enemy_bullet.y > HEIGHT:
            enemy_bullets.remove(enemy_bullet)
        elif enemy_bullet.colliderect(player_rect):
            print("Game Over")
            running = False
            sys.exit()

    # Check if all enemies are destroyed
    if not enemies:
        level += 1
        bullet_cooldown = 500 - (level * 50)  # Decrease bullet cooldown with each level
        enemy_bullet_cooldown = 500 - (level * 50)  # Decrease enemy bullet cooldown with each level

        # Reset player and enemy positions
        player_rect.x = WIDTH // 2 - player_rect.width // 2
        player_rect.y = HEIGHT - player_rect.height - 10
        for row in range(num_rows):
            for col in range(num_cols):
                enemy = enemy_rect.copy()
                enemy.x = 50 + col * (enemy_rect.width + enemy_spacing)
                enemy.y = 50 + row * (enemy_rect.height + enemy_spacing)
                enemies.append(enemy)

        # Reset bullet times
        last_bullet_time = pygame.time.get_ticks() - bullet_cooldown
        last_enemy_bullet_time = pygame.time.get_ticks() - enemy_bullet_cooldown

    # Render objects
    window.blit(background, (0, 0))

    window.blit(playerImg, player_rect)
    for bullet in bullets:
        window.blit(bulletImg, bullet)
    for enemy_bullet in enemy_bullets:
        window.blit(enemy_bulletImg, enemy_bullet)
    for enemy in enemies:
        window.blit(enemyImg, enemy)

    for bullet in bullets:
        bullet.y -= 5
        if bullet.y < 0:
            bullets.remove(bullet)
        else:
            for enemy in enemies:
                if bullet.colliderect(enemy):
                    explosion_Sound = mixer.Sound('Sound/explosion.wav')
                    explosion_Sound.play()
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 10  # Increase the score for  each enemy hit

    for enemy_bullet in enemy_bullets:
        enemy_bullet.y += 5
        if enemy_bullet.y > HEIGHT:
            enemy_bullets.remove(enemy_bullet)
        elif enemy_bullet.colliderect(player_rect):
            print("Game Over")
            running = False
            sys.exit()


    # Check if all enemies are destroyed
    if not enemies:
        level += 1
        bullet_cooldown = 500 - (level * 50)  # Decrease bullet cooldown with each level
        enemy_bullet_cooldown = 500 - (level * 50)  # Decrease enemy bullet cooldown with each level

        # Reset player and enemy positions
        player_rect.x = WIDTH // 2 - player_rect.width // 2
        player_rect.y = HEIGHT - player_rect.height - 10
        for row in range(num_rows):
            for col in range(num_cols):
                enemy = enemy_rect.copy()
                enemy.x = 50 + col * (enemy_rect.width + enemy_spacing)
                enemy.y = 50 + row * (enemy_rect.height + enemy_spacing)
                enemies.append(enemy)

        # Reset bullet times
        last_bullet_time = pygame.time.get_ticks() - bullet_cooldown
        last_enemy_bullet_time = pygame.time.get_ticks() - enemy_bullet_cooldown

    # Render objects
    window.blit(background, (0, 0))

    window.blit(playerImg, player_rect)
    for bullet in bullets:
        window.blit(bulletImg, bullet)
    for enemy_bullet in enemy_bullets:
        window.blit(enemy_bulletImg, enemy_bullet)
    for enemy in enemies:
        window.blit(enemyImg, enemy)

    # Display level and score on the screen
    font = pygame.font.Font(None, 36)
    level_text = font.render("Level: " + str(level), True, WHITE)
    score_text = font.render("Score: " + str(score), True, WHITE)
    window.blit(level_text, (10, 10))
    window.blit(score_text, (10, 50))

    pygame.display.update()