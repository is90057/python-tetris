import pygame
import random
import os

# Initialize pygame and mixer
pygame.init()
pygame.mixer.init()

# Setup Screen Constants
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
SCREEN_WIDTH = GRID_WIDTH * BLOCK_SIZE + 200 # Extra space for score/next piece
SCREEN_HEIGHT = GRID_HEIGHT * BLOCK_SIZE

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris with Sounds")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
GRID_COLOR = (40, 40, 40)
TEXT_COLOR = (200, 200, 200)

COLORS = [
    (0, 255, 255),    # I - Cyan
    (255, 165, 0),    # L - Orange
    (0, 0, 255),      # J - Blue
    (255, 255, 0),    # O - Yellow
    (0, 255, 0),      # S - Green
    (128, 0, 128),    # T - Purple
    (255, 0, 0)       # Z - Red
]

# Tetromino Definitions
SHAPES = [
    [[1, 1, 1, 1]], # I
    [[1, 0, 0],
     [1, 1, 1]],    # J
    [[0, 0, 1],
     [1, 1, 1]],    # L
    [[1, 1],
     [1, 1]],       # O
    [[0, 1, 1],
     [1, 1, 0]],    # S
    [[0, 1, 0],
     [1, 1, 1]],    # T
    [[1, 1, 0],
     [0, 1, 1]]     # Z
]

# Load Sounds
def load_sound(name):
    path = os.path.join(os.path.dirname(__file__), name)
    if os.path.exists(path):
        return pygame.mixer.Sound(path)
    else:
        # Dummy sound class if missing
        class DummySound:
            def play(self): pass
        return DummySound()

sounds = {
    'move': load_sound('move.wav'),
    'rotate': load_sound('rotate.wav'),
    'drop': load_sound('drop.wav'),
    'clear': load_sound('clear.wav'),
    'gameover': load_sound('gameover.wav')
}

font = pygame.font.SysFont('consolas', 24)
large_font = pygame.font.SysFont('consolas', 36)

class Tetromino:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.shape_idx = random.randint(0, len(SHAPES) - 1)
        self.shape = SHAPES[self.shape_idx]
        self.color = COLORS[self.shape_idx]

    def rotate(self):
        # Rotate 90 degrees clockwise
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

class Tetris:
    def __init__(self):
        self.grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        self.current = Tetromino(3, 0)
        self.next = Tetromino(3, 0)
        self.score = 0
        self.game_over = False

    def new_piece(self):
        self.current = self.next
        self.current.x = 3
        self.current.y = 0
        self.next = Tetromino(3, 0)
        if self.check_collision(1, 0):
            self.game_over = True
            sounds['gameover'].play()

    def check_collision(self, dy, dx, shape=None):
        shape = shape or self.current.shape
        for r, row in enumerate(shape):
            for c, val in enumerate(row):
                if val:
                    nx = self.current.x + dx + c
                    ny = self.current.y + dy + r
                    if nx < 0 or nx >= GRID_WIDTH or ny >= GRID_HEIGHT:
                        return True
                    if ny >= 0 and self.grid[ny][nx] != 0:
                        return True
        return False

    def lock_piece(self):
        sounds['drop'].play()
        for r, row in enumerate(self.current.shape):
            for c, val in enumerate(row):
                if val:
                    # check if gameover when locking off-screen somehow
                    if self.current.y + r < 0:
                        self.game_over = True
                        sounds['gameover'].play()
                        return
                    self.grid[self.current.y + r][self.current.x + c] = self.current.color
        self.clear_lines()
        if not self.game_over:
            self.new_piece()

    def clear_lines(self):
        lines_to_clear = []
        for r in range(GRID_HEIGHT):
            if all(self.grid[r]):
                lines_to_clear.append(r)
        
        if lines_to_clear:
            sounds['clear'].play()
            for r in lines_to_clear:
                del self.grid[r]
                self.grid.insert(0, [0] * GRID_WIDTH)
            self.score += (len(lines_to_clear) ** 2) * 100

def draw_text_middle(text, size, color, surface):
    font_temp = pygame.font.SysFont('consolas', size, bold=True)
    label = font_temp.render(text, 1, color)
    surface.blit(label, (SCREEN_WIDTH / 2 - label.get_width() / 2, SCREEN_HEIGHT / 2 - label.get_height() / 2))

def draw_window(surface, game):
    surface.fill(BLACK)

    # Draw grid blocks
    for r in range(GRID_HEIGHT):
        for c in range(GRID_WIDTH):
            if game.grid[r][c] != 0:
                pygame.draw.rect(surface, game.grid[r][c], (c * BLOCK_SIZE, r * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    # Draw current piece
    if not game.game_over:
        for r, row in enumerate(game.current.shape):
            for c, val in enumerate(row):
                if val:
                    pygame.draw.rect(surface, game.current.color, ((game.current.x + c) * BLOCK_SIZE, (game.current.y + r) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    # Draw grid lines
    for r in range(GRID_HEIGHT):
        pygame.draw.line(surface, GRID_COLOR, (0, r * BLOCK_SIZE), (GRID_WIDTH * BLOCK_SIZE, r * BLOCK_SIZE))
    for c in range(GRID_WIDTH):
        pygame.draw.line(surface, GRID_COLOR, (c * BLOCK_SIZE, 0), (c * BLOCK_SIZE, SCREEN_HEIGHT))

    # Border around play area
    pygame.draw.rect(surface, WHITE, (0, 0, GRID_WIDTH * BLOCK_SIZE, SCREEN_HEIGHT), 2)

    # Draw Score & Next piece text
    score_label = font.render(f'Score: {game.score}', 1, TEXT_COLOR)
    surface.blit(score_label, (GRID_WIDTH * BLOCK_SIZE + 20, 20))
    
    next_label = font.render('Next:', 1, TEXT_COLOR)
    surface.blit(next_label, (GRID_WIDTH * BLOCK_SIZE + 20, 80))

    # Draw next piece
    next_piece = game.next
    for r, row in enumerate(next_piece.shape):
        for c, val in enumerate(row):
            if val:
                pygame.draw.rect(surface, next_piece.color, (GRID_WIDTH * BLOCK_SIZE + 40 + c * BLOCK_SIZE, 120 + r * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    if game.game_over:
        draw_text_middle('GAME OVER', 60, WHITE, surface)

    pygame.display.update()

def main():
    game = Tetris()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.5 # seconds
    run = True

    while run:
        fall_time += clock.get_rawtime()
        clock.tick(60)

        if not game.game_over and fall_time / 1000 >= fall_speed:
            fall_time = 0
            if not game.check_collision(1, 0):
                game.current.y += 1
            else:
                game.lock_piece()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN and not game.game_over:
                if event.key == pygame.K_LEFT:
                    if not game.check_collision(0, -1):
                        game.current.x -= 1
                        sounds['move'].play()
                elif event.key == pygame.K_RIGHT:
                    if not game.check_collision(0, 1):
                        game.current.x += 1
                        sounds['move'].play()
                elif event.key == pygame.K_DOWN:
                    if not game.check_collision(1, 0):
                        game.current.y += 1
                        sounds['move'].play()
                elif event.key == pygame.K_UP:
                    # Rotate
                    # Store original shape in case collision occurs
                    original_shape = game.current.shape
                    game.current.rotate()
                    if game.check_collision(0, 0):
                        game.current.shape = original_shape
                    else:
                        sounds['rotate'].play()
                elif event.key == pygame.K_SPACE:
                    # Hard drop
                    while not game.check_collision(1, 0):
                        game.current.y += 1
                    game.lock_piece()

        draw_window(screen, game)

    pygame.quit()

if __name__ == '__main__':
    main()
