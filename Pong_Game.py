import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
BALL_SIZE = 15
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 90
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")
clock = pygame.time.Clock()

ball_x, ball_y = WIDTH // 2, HEIGHT // 2
ball_dx, ball_dy = 5, 5

paddle1_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
paddle2_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
paddle_speed = 7

score1, score2 = 0, 0
font = pygame.font.Font(None, 74)

def reset_ball():
    global ball_x, ball_y, ball_dx, ball_dy
    ball_x, ball_y = WIDTH // 2, HEIGHT // 2
    ball_dx = 5 if ball_dx > 0 else -5
    ball_dy = 5 if ball_dy > 0 else -5

def draw_objects():
    screen.fill(BLACK)
  
    for i in range(0, HEIGHT, 20):
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 2, i, 4, 10))
    
    pygame.draw.rect(screen, WHITE, (30, paddle1_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(screen, WHITE, (WIDTH - 30 - PADDLE_WIDTH, paddle2_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    
    pygame.draw.circle(screen, WHITE, (int(ball_x), int(ball_y)), BALL_SIZE)

    score_text1 = font.render(str(score1), True, WHITE)
    score_text2 = font.render(str(score2), True, WHITE)
    screen.blit(score_text1, (WIDTH // 4, 30))
    screen.blit(score_text2, (3 * WIDTH // 4 - score_text2.get_width(), 30))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_w] and paddle1_y > 0:
        paddle1_y -= paddle_speed
    if keys[pygame.K_s] and paddle1_y < HEIGHT - PADDLE_HEIGHT:
        paddle1_y += paddle_speed
    
    if keys[pygame.K_UP] and paddle2_y > 0:
        paddle2_y -= paddle_speed
    if keys[pygame.K_DOWN] and paddle2_y < HEIGHT - PADDLE_HEIGHT:
        paddle2_y += paddle_speed
    
    ball_x += ball_dx
    ball_y += ball_dy
    
    if ball_y - BALL_SIZE <= 0 or ball_y + BALL_SIZE >= HEIGHT:
        ball_dy *= -1
    
    if (ball_x - BALL_SIZE <= 30 + PADDLE_WIDTH and 
        paddle1_y <= ball_y <= paddle1_y + PADDLE_HEIGHT and
        ball_dx < 0):
        ball_dx *= -1

        hit_pos = (ball_y - paddle1_y) / PADDLE_HEIGHT
        ball_dy = (hit_pos - 0.5) * 10
    
    if (ball_x + BALL_SIZE >= WIDTH - 30 - PADDLE_WIDTH and 
        paddle2_y <= ball_y <= paddle2_y + PADDLE_HEIGHT and
        ball_dx > 0):
        ball_dx *= -1
        hit_pos = (ball_y - paddle2_y) / PADDLE_HEIGHT
        ball_dy = (hit_pos - 0.5) * 10
    
    if ball_x < 0:
        score2 += 1
        reset_ball()
        pygame.time.delay(500)
    elif ball_x > WIDTH:
        score1 += 1
        reset_ball()
        pygame.time.delay(500)
    
    draw_objects()
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()