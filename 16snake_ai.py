import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GRAY = (40, 40, 40)  # Grid color

# Game settings
DIS_WIDTH = 800
DIS_HEIGHT = 600
SNAKE_BLOCK = 20
clock = pygame.time.Clock()

# AI Speed settings
LEVEL_SPEEDS = {"Easy": 6, "Normal": 7, "Hard": 7}
PLAYER_SPEED = 12  # Player speed is constant

# Display setup
dis = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
pygame.display.set_caption('AI Snake Game')

# Fonts
score_font = pygame.font.SysFont("comicsansms", 35)
menu_font = pygame.font.SysFont("bahnschrift", 30)

# Load Sounds (use None if files don't exist to prevent errors)
try:
    eat_sound = pygame.mixer.Sound(r"C:\pragati\codes\python language\python projects\eat.wav")
except:
    eat_sound = None
try:
    game_over_sound = pygame.mixer.Sound(r"C:\pragati\codes\python language\python projects\game_over.wav")
except:
    game_over_sound = None

# Function to display score
def show_score(player_score, ai_score):
    player_text = score_font.render(f"Player Score: {player_score}", True, YELLOW)
    ai_text = score_font.render(f"AI Score: {ai_score}", True, RED)
    dis.blit(player_text, [10, 10])
    dis.blit(ai_text, [10, 50])

# Function to generate random food position
def generate_food():
    return (
        random.randrange(0, DIS_WIDTH, SNAKE_BLOCK),
        random.randrange(0, DIS_HEIGHT, SNAKE_BLOCK)
    )

# AI movement logic
def ai_move_towards_food(ai_x, ai_y, food_x, food_y, difficulty):
    if difficulty == "Hard":  # Allow diagonal movement only in Hard mode
        if ai_x < food_x:
            ai_x += SNAKE_BLOCK
        elif ai_x > food_x:
            ai_x -= SNAKE_BLOCK
        if ai_y < food_y:
            ai_y += SNAKE_BLOCK
        elif ai_y > food_y:
            ai_y -= SNAKE_BLOCK
    else:  # Restrict to horizontal or vertical movement only
        if ai_x != food_x:
            ai_x += SNAKE_BLOCK if ai_x < food_x else -SNAKE_BLOCK
        elif ai_y != food_y:
            ai_y += SNAKE_BLOCK if ai_y < food_y else -SNAKE_BLOCK
    return ai_x, ai_y

# Function to show level selection menu
def level_selection_menu():
    while True:
        dis.fill(BLACK)
        options = ["1 - Easy", "2 - Normal", "3 - Hard"]
        title = menu_font.render("Select Level:", True, WHITE)
        dis.blit(title, (DIS_WIDTH // 2 - title.get_width() // 2, DIS_HEIGHT // 3))
        
        for i, option in enumerate(options):
            text = menu_font.render(option, True, YELLOW)
            dis.blit(text, (DIS_WIDTH // 2 - text.get_width() // 2, DIS_HEIGHT // 3 + 50 * (i + 1)))
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "Easy"
                elif event.key == pygame.K_2:
                    return "Normal"
                elif event.key == pygame.K_3:
                    return "Hard"

# Function to draw grid
def draw_grid():
    for x in range(0, DIS_WIDTH, SNAKE_BLOCK):
        pygame.draw.line(dis, GRAY, (x, 0), (x, DIS_HEIGHT))
    for y in range(0, DIS_HEIGHT, SNAKE_BLOCK):
        pygame.draw.line(dis, GRAY, (0, y), (DIS_WIDTH, y))

# Game loop
def game_loop(difficulty):
    player_score = ai_score = 0
    player_x, player_y = generate_food()
    ai_x, ai_y = generate_food()
    food_x, food_y = generate_food()
    player_dx = player_dy = 0  
    ai_frame_counter = 0
    ai_speed = LEVEL_SPEEDS[difficulty]
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_dx, player_dy = -SNAKE_BLOCK, 0
                elif event.key == pygame.K_RIGHT:
                    player_dx, player_dy = SNAKE_BLOCK, 0
                elif event.key == pygame.K_UP:
                    player_dx, player_dy = 0, -SNAKE_BLOCK
                elif event.key == pygame.K_DOWN:
                    player_dx, player_dy = 0, SNAKE_BLOCK
        
        player_x += player_dx
        player_y += player_dy

        if player_x < 0 or player_x >= DIS_WIDTH or player_y < 0 or player_y >= DIS_HEIGHT:
            if game_over_sound:
                pygame.mixer.Sound.play(game_over_sound)
            return game_over_screen(player_score, ai_score)
        
        if ai_frame_counter % (PLAYER_SPEED // ai_speed) == 0:
            ai_x, ai_y = ai_move_towards_food(ai_x, ai_y, food_x, food_y, difficulty)
        
        if player_x == food_x and player_y == food_y:
            player_score += 1
            if eat_sound:
                pygame.mixer.Sound.play(eat_sound)
            food_x, food_y = generate_food()
        
        if ai_x == food_x and ai_y == food_y:
            ai_score += 1
            food_x, food_y = generate_food()
        
        dis.fill(BLACK)
        draw_grid()
        show_score(player_score, ai_score)
        pygame.draw.rect(dis, WHITE, [food_x, food_y, SNAKE_BLOCK, SNAKE_BLOCK])
        pygame.draw.rect(dis, YELLOW, [player_x, player_y, SNAKE_BLOCK, SNAKE_BLOCK])
        pygame.draw.rect(dis, RED, [ai_x, ai_y, SNAKE_BLOCK, SNAKE_BLOCK])

        pygame.display.update()
        ai_frame_counter += 1
        clock.tick(PLAYER_SPEED)

# Function to show Game Over screen
def game_over_screen(player_score, ai_score):
    dis.fill(BLACK)
    game_over_text = score_font.render("Game Over!", True, RED)
    score_text = score_font.render(f"Final Scores - Player: {player_score} | AI: {ai_score}", True, WHITE)
    restart_text = score_font.render("Press R to Restart or Q to Quit", True, YELLOW)
    
    dis.blit(game_over_text, game_over_text.get_rect(center=(DIS_WIDTH // 2, DIS_HEIGHT // 2 - 60)))
    dis.blit(score_text, score_text.get_rect(center=(DIS_WIDTH // 2, DIS_HEIGHT // 2)))
    dis.blit(restart_text, restart_text.get_rect(center=(DIS_WIDTH // 2, DIS_HEIGHT // 2 + 60)))
    
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_r:
                    return  # Return to main menu

# Main game function
def main():
    while True:
        difficulty = level_selection_menu()
        game_loop(difficulty)

if __name__ == "__main__":
    main()