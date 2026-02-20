import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 1000, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Endless Red Ball")

clock = pygame.time.Clock()

SKY = (135, 206, 250)
GRASS = (50, 200, 50)
DIRT = (139, 69, 19)
RED = (220, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 215, 0)
BROWN = (120, 70, 20)

font = pygame.font.SysFont(None, 40)
big_font = pygame.font.SysFont(None, 70)

radius = 25
gravity = 0.8
jump_power = -15
speed = 6

def reset_game():
    global player_x, player_y, vel_y
    global platforms, last_x, camera_x
    global game_over, score
    global stars, boxes, clouds

    player_x = 100
    player_y = 350
    vel_y = 0
    camera_x = 0
    game_over = False
    score = 0

    platforms = []
    stars = []
    boxes = []

    platforms.append(pygame.Rect(0, 400, 1000, 100))
    last_x = 1000

    clouds = []
    for i in range(5):
        clouds.append([random.randint(0, WIDTH),
                       random.randint(50, 200),
                       random.randint(60, 120)])

def generate_land():
    global last_x

    gap = random.randint(80, 120)
    width = random.randint(200, 400)

    new_platform = pygame.Rect(
        last_x + gap,
        400,
        width,
        100
    )

    platforms.append(new_platform)

    stars.append(pygame.Rect(
        new_platform.x + width//2,
        360,
        20, 20
    ))

    if random.random() < 0.5:
        boxes.append(pygame.Rect(
            new_platform.x + random.randint(40, width-60),
            360,
            40, 40
        ))

    last_x = new_platform.x + width

reset_game()

running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if game_over and keys[pygame.K_r]:
        reset_game()

    if not game_over:

        if keys[pygame.K_RIGHT]:
            player_x += speed
        if keys[pygame.K_LEFT]:
            player_x -= speed

        vel_y += gravity
        player_y += vel_y

        player_rect = pygame.Rect(
            player_x - radius,
            player_y - radius,
            radius*2,
            radius*2
        )

        on_ground = False

        for p in platforms:
            if player_rect.colliderect(p):
                if vel_y > 0:
                    player_y = p.top - radius
                    vel_y = 0
                    on_ground = True

        if keys[pygame.K_UP] and on_ground:
            vel_y = jump_power

        if player_y > HEIGHT:
            game_over = True

        while last_x < player_x + 800:
            generate_land()

        for s in stars[:]:
            if player_rect.colliderect(s):
                stars.remove(s)
                score += 10

        for b in boxes:
            if player_rect.colliderect(b):
                game_over = True

        score += 0.05
        camera_x = player_x - WIDTH//3

        for cloud in clouds:
            cloud[0] -= 0.5
            if cloud[0] < -150:
                cloud[0] = WIDTH + 100

    screen.fill(SKY)

    for cloud in clouds:
        pygame.draw.ellipse(screen, WHITE,
            (cloud[0], cloud[1], cloud[2], 50))

    for p in platforms:
        pygame.draw.rect(screen, DIRT,
            (p.x - camera_x, p.y, p.width, p.height))
        pygame.draw.rect(screen, GRASS,
            (p.x - camera_x, p.y - 10, p.width, 10))

    for s in stars:
        pygame.draw.circle(screen, YELLOW,
            (int(s.x - camera_x + 10), s.y + 10), 10)

    for b in boxes:
        pygame.draw.rect(screen, BROWN,
            (b.x - camera_x, b.y, b.width, b.height))

    if not game_over:
        pygame.draw.circle(screen, RED,
            (int(player_x - camera_x), int(player_y)), radius)

    score_text = font.render(f"Score: {int(score)}", True, BLACK)
    screen.blit(score_text, (20, 20))

    if game_over:
        text = big_font.render("GAME OVER", True, BLACK)
        screen.blit(text, (WIDTH//2 - text.get_width()//2, 200))

        restart = font.render("Press R to Restart", True, BLACK)
        screen.blit(restart, (WIDTH//2 - restart.get_width()//2, 260))

    pygame.display.update()

pygame.quit()
sys.exit()
