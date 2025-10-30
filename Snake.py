import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (231, 76, 60)
GREEN = (46, 204, 113)
BLUE = (52, 152, 219)
DARK_GREEN = (39, 174, 96)
GRAY = (149, 165, 166)
YELLOW = (241, 196, 15)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Snake:
    def __init__(self):
        self.length = 3
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.color = GREEN
        self.head_color = DARK_GREEN
        self.score = 0
        
    def get_head_position(self):
        return self.positions[0]
    
    def update(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = ((cur[0] + x) % GRID_WIDTH, (cur[1] + y) % GRID_HEIGHT)
        
        # Check if snake hits itself
        if len(self.positions) > 2 and new in self.positions[2:]:
            return False
        
        self.positions.insert(0, new)
        if len(self.positions) > self.length:
            self.positions.pop()
        
        return True
    
    def reset(self):
        self.length = 3
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.score = 0
    
    def render(self, surface):
        for i, pos in enumerate(self.positions):
            rect = pygame.Rect(pos[0] * GRID_SIZE, pos[1] * GRID_SIZE, 
                             GRID_SIZE - 2, GRID_SIZE - 2)
            if i == 0:  # Head
                pygame.draw.rect(surface, self.head_color, rect)
                pygame.draw.rect(surface, WHITE, rect, 2)
                # Draw eyes
                eye_size = 3
                left_eye = (pos[0] * GRID_SIZE + 5, pos[1] * GRID_SIZE + 5)
                right_eye = (pos[0] * GRID_SIZE + GRID_SIZE - 8, pos[1] * GRID_SIZE + 5)
                pygame.draw.circle(surface, BLACK, left_eye, eye_size)
                pygame.draw.circle(surface, BLACK, right_eye, eye_size)
            else:  # Body
                pygame.draw.rect(surface, self.color, rect)
                pygame.draw.rect(surface, DARK_GREEN, rect, 1)

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()
    
    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1),
                        random.randint(0, GRID_HEIGHT - 1))
    
    def render(self, surface):
        rect = pygame.Rect(self.position[0] * GRID_SIZE, 
                          self.position[1] * GRID_SIZE,
                          GRID_SIZE - 2, GRID_SIZE - 2)
        pygame.draw.rect(surface, self.color, rect)
        pygame.draw.rect(surface, YELLOW, rect, 2)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Snake Game - Use Arrow Keys')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.large_font = pygame.font.Font(None, 72)
        self.snake = Snake()
        self.food = Food()
        self.running = True
        self.paused = False
        self.game_over = False
        self.fps = 10
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_RETURN:
                        self.reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
                else:
                    if event.key == pygame.K_UP and self.snake.direction != DOWN:
                        self.snake.direction = UP
                    elif event.key == pygame.K_DOWN and self.snake.direction != UP:
                        self.snake.direction = DOWN
                    elif event.key == pygame.K_LEFT and self.snake.direction != RIGHT:
                        self.snake.direction = LEFT
                    elif event.key == pygame.K_RIGHT and self.snake.direction != LEFT:
                        self.snake.direction = RIGHT
                    elif event.key == pygame.K_SPACE:
                        self.paused = not self.paused
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
    
    def update(self):
        if not self.paused and not self.game_over:
            # Update snake
            if not self.snake.update():
                self.game_over = True
                return
            
            # Check if snake ate food
            if self.snake.get_head_position() == self.food.position:
                self.snake.length += 1
                self.snake.score += 10
                self.food.randomize_position()
                
                # Make sure food doesn't spawn on snake
                while self.food.position in self.snake.positions:
                    self.food.randomize_position()
                
                # Increase speed slightly
                if self.snake.score % 50 == 0 and self.fps < 20:
                    self.fps += 1
    
    def render(self):
        self.screen.fill(BLACK)
        
        # Draw grid
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, WINDOW_HEIGHT), 1)
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, GRAY, (0, y), (WINDOW_WIDTH, y), 1)
        
        # Draw game objects
        self.snake.render(self.screen)
        self.food.render(self.screen)
        
        # Draw score
        score_text = self.font.render(f'Score: {self.snake.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Draw speed indicator
        speed_text = self.font.render(f'Speed: {self.fps}', True, WHITE)
        self.screen.blit(speed_text, (WINDOW_WIDTH - 150, 10))
        
        # Draw pause indicator
        if self.paused:
            pause_text = self.large_font.render('PAUSED', True, YELLOW)
            text_rect = pause_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            self.screen.blit(pause_text, text_rect)
            
            resume_text = self.font.render('Press SPACE to resume', True, WHITE)
            resume_rect = resume_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
            self.screen.blit(resume_text, resume_rect)
        
        # Draw game over screen
        if self.game_over:
            # Semi-transparent overlay
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(200)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            game_over_text = self.large_font.render('GAME OVER!', True, RED)
            game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
            self.screen.blit(game_over_text, game_over_rect)
            
            final_score_text = self.font.render(f'Final Score: {self.snake.score}', True, WHITE)
            score_rect = final_score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))
            self.screen.blit(final_score_text, score_rect)
            
            restart_text = self.font.render('Press ENTER to play again', True, GREEN)
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 70))
            self.screen.blit(restart_text, restart_rect)
            
            quit_text = self.font.render('Press ESC to quit', True, GRAY)
            quit_rect = quit_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 110))
            self.screen.blit(quit_text, quit_rect)
        
        pygame.display.flip()
    
    def reset_game(self):
        self.snake.reset()
        self.food.randomize_position()
        self.game_over = False
        self.paused = False
        self.fps = 10
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(self.fps)
        
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = Game()
    game.run()
