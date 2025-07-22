
import pygame
import sys
import random
from grid import Grid

pygame.init()

# Colors
dark_blue = (44, 44, 127)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Screen setup
screen = pygame.display.set_mode((600, 700))  # Extra space for UI
pygame.display.set_caption("Snake and Ladder Game")

clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 24)

# Game setup
game_grid = Grid()
dice_value = 1
current_player = 1  # 1 or 2
game_over = False
winner = None

# Player positions (start at 0 which is before position 1)
player_positions = {1: 0, 2: 0}

# Snakes and Ladders (start: end)
snakes_ladders = {
    # Ladders
    4: 14,
    9: 31,
    20: 38,
    28: 84,
    40: 59,
    51: 67,
    63: 81,
    71: 91,
    
    # Snakes
    17: 7,
    54: 34,
    62: 19,
    64: 60,
    87: 24,
    93: 73,
    95: 75,
    99: 78
}

def roll_dice():
    return random.randint(1, 6)

def move_player(player, steps):
    global current_player, game_over, winner
    
    player_positions[player] += steps
    
    # Check if player won
    if player_positions[player] >= 100:
        player_positions[player] = 100
        game_over = True
        winner = player
        return
    
    # Check for snakes or ladders
    if player_positions[player] in snakes_ladders:
        player_positions[player] = snakes_ladders[player_positions[player]]
    
    # Switch player if not 6
    if steps != 6:
        current_player = 2 if current_player == 1 else 1

def draw_ui():
    # Draw current player info
    player_text = f"Player {current_player}'s turn"
    text_surface = font.render(player_text, True, BLUE if current_player == 1 else RED)
    screen.blit(text_surface, (20, 610))
    
    # Draw dice
    pygame.draw.rect(screen, WHITE, (250, 610, 100, 100))
    pygame.draw.rect(screen, BLACK, (250, 610, 100, 100), 2)
    
    # Draw dice value
    dice_text = font.render(str(dice_value), True, BLACK)
    screen.blit(dice_text, (290, 650))
    
    # Draw roll instruction
    roll_text = font.render("Press SPACE to roll", True, WHITE)
    screen.blit(roll_text, (400, 650))
    
    # Draw player positions
    pos_text = f"Player 1: {player_positions[1]} | Player 2: {player_positions[2]}"
    pos_surface = font.render(pos_text, True, WHITE)
    screen.blit(pos_surface, (20, 650))
    
    # Draw winner message
    if game_over:
        winner_text = font.render(f"Player {winner} wins!", True, YELLOW)
        screen.blit(winner_text, (200, 680))

def draw_players():
    for player, pos in player_positions.items():
        if pos == 0:
            continue  # Not on board yet
        
        # Convert position to row and column (snake pattern)
        row = 9 - (pos - 1) // 10
        if row % 2 == 1:
            col = (pos - 1) % 10
        else:
            col = 9 - (pos - 1) % 10
        
        # Draw player
        x = col * game_grid.cell_size + game_grid.cell_size // 2
        y = row * game_grid.cell_size + game_grid.cell_size // 2
        color = BLUE if player == 1 else RED
        pygame.draw.circle(screen, color, (x, y), game_grid.cell_size // 3)

def draw_snakes_ladders():
    for start, end in snakes_ladders.items():
        # Get positions
        start_row = 9 - (start - 1) // 10
        if start_row % 2 == 1:
            start_col = (start - 1) % 10
        else:
            start_col = 9 - (start - 1) % 10
        
        end_row = 9 - (end - 1) // 10
        if end_row % 2 == 1:
            end_col = (end - 1) % 10
        else:
            end_col = 9 - (end - 1) % 10
        
        # Calculate pixel positions
        start_x = start_col * game_grid.cell_size + game_grid.cell_size // 2
        start_y = start_row * game_grid.cell_size + game_grid.cell_size // 2
        end_x = end_col * game_grid.cell_size + game_grid.cell_size // 2
        end_y = end_row * game_grid.cell_size + game_grid.cell_size // 2
        
        # Draw line (green for ladders, red for snakes)
        color = GREEN if start < end else RED
        pygame.draw.line(screen, color, (start_x, start_y), (end_x, end_y), 3)

def draw_numbers():
    for i in range(1, 101):
        row = 9 - (i - 1) // 10
        if row % 2 == 1:
            col = (i - 1) % 10
        else:
            col = 9 - (i - 1) % 10
        
        x = col * game_grid.cell_size + 5
        y = row * game_grid.cell_size + 5
        num_text = font.render(str(i), True, BLACK)
        screen.blit(num_text, (x, y))

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                dice_value = roll_dice()
                move_player(current_player, dice_value)
    
    # Drawing
    screen.fill(dark_blue)
    game_grid.draw(screen)
    draw_snakes_ladders()
    draw_numbers()
    draw_players()
    draw_ui()
    
    pygame.display.update()
    clock.tick(60)
