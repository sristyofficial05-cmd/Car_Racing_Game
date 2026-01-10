import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bike Racing Game with Power-Up")

# Load images
bike_img = pygame.image.load("bike.png")
enemy_bike_img = pygame.image.load("enemy_bike.png")
enemy_car_img = pygame.image.load("enemy_car.png")
road_img = pygame.image.load("road.png")
shield_img = pygame.image.load("shield.png")

# Resize images
bike_img = pygame.transform.scale(bike_img, (50, 100))
enemy_bike_img = pygame.transform.scale(enemy_bike_img, (50, 100))
enemy_car_img = pygame.transform.scale(enemy_car_img, (50, 100))
road_img = pygame.transform.scale(road_img, (WIDTH, HEIGHT))
shield_img = pygame.transform.scale(shield_img, (40, 40))

# Clock and font
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

# Draw text
def draw_text(text, x, y, color=(255, 255, 255)):
    screen.blit(font.render(text, True, color), (x, y))

# Loading screen
def show_loading_screen():
    screen.fill((0, 0, 0))
    draw_text("Loading Game...", WIDTH // 2 - 120, HEIGHT // 2, (255, 255, 0))
    pygame.display.update()
    pygame.time.delay(1500)

# Game Over screen with restart/quit
def show_game_over(score):
    screen.fill((0, 0, 0))
    draw_text("GAME OVER", WIDTH // 2 - 100, HEIGHT // 2 - 60, (255, 0, 0))
    draw_text(f"Your Score: {score}", WIDTH // 2 - 100, HEIGHT // 2 - 20, (255, 255, 255))
    draw_text("Press R to Restart or Q to Quit", WIDTH // 2 - 180, HEIGHT // 2 + 30)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                elif event.key == pygame.K_q:
                    pygame.quit(); sys.exit()

# Main game function
def run_game():
    player_x = WIDTH // 2 - 25
    player_y = HEIGHT - 120
    player_speed = 7
    shield_active = False
    score = 0

    # Enemies
    enemy_list = []
    enemy_speed = 5
    for _ in range(3):
        img = random.choice([enemy_bike_img, enemy_car_img])
        x = random.randint(100, WIDTH - 100)
        y = random.randint(-600, -100)
        enemy_list.append({'img': img, 'x': x, 'y': y})

    # Shield power-up
    shield_x = random.randint(100, WIDTH - 100)
    shield_y = -300
    shield_speed = 4

    # Road scrolling
    road_y = 0

    running = True
    while running:
        screen.fill((0, 0, 0))

        # Scroll road
        road_y += 5
        if road_y >= HEIGHT:
            road_y = 0
        screen.blit(road_img, (0, road_y - HEIGHT))
        screen.blit(road_img, (0, road_y))

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Key press
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - 50:
            player_x += player_speed
        if keys[pygame.K_UP] and player_y > 0:
            player_y -= player_speed
        if keys[pygame.K_DOWN] and player_y < HEIGHT - 100:
            player_y += player_speed

        # Draw player
        screen.blit(bike_img, (player_x, player_y))

        # Move enemies
        player_rect = pygame.Rect(player_x, player_y, 50, 100)
        for enemy in enemy_list:
            enemy['y'] += enemy_speed
            if enemy['y'] > HEIGHT:
                enemy['y'] = random.randint(-600, -100)
                enemy['x'] = random.randint(100, WIDTH - 100)
                enemy['img'] = random.choice([enemy_bike_img, enemy_car_img])
                score += 1
            screen.blit(enemy['img'], (enemy['x'], enemy['y']))

            # Collision
            enemy_rect = pygame.Rect(enemy['x'], enemy['y'], 50, 100)
            if player_rect.colliderect(enemy_rect):
                if shield_active:
                    shield_active = False
                    enemy['y'] = -100
                else:
                    return score  # Game over

        # Move shield
        shield_y += shield_speed
        if shield_y > HEIGHT:
            shield_x = random.randint(100, WIDTH - 100)
            shield_y = -random.randint(300, 600)
        screen.blit(shield_img, (shield_x, shield_y))

        # Collect shield
        shield_rect = pygame.Rect(shield_x, shield_y, 40, 40)
        if player_rect.colliderect(shield_rect):
            shield_active = True
            shield_y = -random.randint(300, 600)

        # Score and status
        draw_text(f"Score: {score}", 10, 10)
        draw_text("🛡️ Shield: ON" if shield_active else "🛡️ Shield: OFF", 10, 50,
                  (0, 255, 0) if shield_active else (255, 0, 0))

        pygame.display.update()
        clock.tick(60)

# Show loading, run game, allow restart
while True:
    show_loading_screen()
    score = run_game()
    if not show_game_over(score):
        break

