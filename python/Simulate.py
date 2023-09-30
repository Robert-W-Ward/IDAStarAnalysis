import sys
import pygame

# Initialize pygame
pygame.init()

class Puzzle:
    def __init__(self, initial_state):
        self.state = initial_state
        self.font = pygame.font.Font(None, 74)
        for i in range(4):
            for j in range(4):
                if self.state[i][j] == 0:
                    self.blank_pos = [i, j]

    def move(self, direction):
        i, j = self.blank_pos
        if direction == 'U' and i > 0:
            self.state[i][j], self.state[i-1][j] = self.state[i-1][j], self.state[i][j]
            self.blank_pos = [i-1, j]
        elif direction == 'D' and i < 3:
            self.state[i][j], self.state[i+1][j] = self.state[i+1][j], self.state[i][j]
            self.blank_pos = [i+1, j]
        elif direction == 'L' and j > 0:
            self.state[i][j], self.state[i][j-1] = self.state[i][j-1], self.state[i][j]
            self.blank_pos = [i, j-1]
        elif direction == 'R' and j < 3:
            self.state[i][j], self.state[i][j+1] = self.state[i][j+1], self.state[i][j]
            self.blank_pos = [i, j+1]

    def draw(self, screen):
        for i in range(4):
            for j in range(4):
                num = self.state[i][j]
                if num != 0:
                    text = self.font.render(str(num), True, (0, 0, 0))
                    pygame.draw.rect(screen, (255, 255, 255), (j * 100, i * 100, 100, 100), 0)
                    screen.blit(text, (j * 100 + 30, i * 100 + 30))
                pygame.draw.rect(screen, (0, 0, 0), (j * 100, i * 100, 100, 100), 1)


# Define initial state
initial_state = [
    [7, 5, 2, 13],
    [1, 8, 11, 0],
    [3, 10, 12, 6],
    [4, 15, 14, 9]
]

# Create a puzzle object
puzzle = Puzzle(initial_state)

# Define moves
moves = "U L D R D L U L U L D R D R D L L U R D R R U U L U L D D D R U L D L U R D R U U L D R R U L U R D L L U R D D L U R R D D".split()

# Set up the display
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption('15 Puzzle Game')

# Main game loop
clock = pygame.time.Clock()
for move in moves:
    puzzle.move(move)
    for _ in range(30):  # Number of frames per move
        screen.fill((0, 0, 0))
        puzzle.draw(screen)
        pygame.display.flip()
        clock.tick(30)  # Frames per second
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# Quit pygame
pygame.quit()
