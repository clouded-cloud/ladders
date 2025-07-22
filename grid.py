
import pygame

class Grid:
    def __init__(self):
        self.cell_size = 60  # Each cell is 60x60 pixels
        self.rows = 10
        self.cols = 10
        self.width = self.cols * self.cell_size
        self.height = self.rows * self.cell_size
        self.colors = [(200, 200, 200), (150, 150, 150)]  # Light and dark cell colors

    def draw(self, screen):
        """Draw the 10x10 grid with alternating colors"""
        for row in range(self.rows):
            for col in range(self.cols):
                # Alternate colors in checkerboard pattern
                color_index = (row + col) % 2
                rect = pygame.Rect(
                    col * self.cell_size,
                    row * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                pygame.draw.rect(screen, self.colors[color_index], rect)
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # Border