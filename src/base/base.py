from global_settings import ROWS, COLS, GAP
import pygame


class Cell:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.start = False
        self.wall = False
        self.target = False
        self.queue = False
        self.visited = False
        self.neighbors = []
        self.prior = None

    def draw(self, screen, color):
        pygame.draw.rect(screen, color, (self.x * GAP, self.y * GAP, GAP - 2, GAP - 2))

    def set_neighbors(self, grid):
        if self.x > 0:
            self.neighbors.append(grid[self.y][self.x - 1])  # Right
        if self.x < COLS - 1:
            self.neighbors.append(grid[self.y][self.x + 1])  # Left
        if self.y > 0:
            self.neighbors.append(grid[self.y - 1][self.x])  # Up
        if self.y < ROWS - 1:
            self.neighbors.append(grid[self.y + 1][self.x])  # Down

    def set_default(self):
        self.start = False
        self.wall = False
        self.target = False
        self.queue = False
        self.visited = False
        self.prior = None
        self.flag = False
