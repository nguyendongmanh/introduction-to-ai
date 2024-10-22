import pygame
from tkinter import messagebox, Tk
import sys
from heapq import *
from global_settings import *
from src.maze.gen_maze import gen_maze
from src.utils.utils import heuristic
from src.base.base import Cell
from src.search.search import Search

pygame.init()
sc = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Path Finding Algorithms")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Calibri", 24)


def draw(grid, path):
    for y in range(ROWS):
        for x in range(COLS):
            cell = grid[y][x]
            cell.draw(sc, COLOR_PATH)

            if cell.queue:
                cell.draw(sc, COLOR_QUEUE)
            if cell.visited:
                cell.draw(sc, COLOR_VISITED)
            if cell in path:
                cell.draw(sc, COLOR_BEST_PATH)

            if cell.start:
                cell.draw(sc, COLOR_START)
            if cell.wall:
                cell.draw(sc, COLOR_WALL)
            if cell.target:
                cell.draw(sc, COLOR_TARGET)

        for i, instruction in enumerate(INSTRUCTIONS):
            text_surface = font.render(instruction, True, WHITE)
            sc.blit(text_surface, (0, WIN_HEIGHT - (len(INSTRUCTIONS) - i) * 20 - 10))


def main():
    import time

    is_printed = False

    grid = []
    # Create grid (dimension = ROWS * COLS)
    for y in range(ROWS):
        arr = []
        for x in range(COLS):
            arr.append(Cell(x, y))  # One arr have items = numbers column
        grid.append(arr)
    # Set all neighbors for each point
    for y in range(ROWS):
        for x in range(COLS):
            grid[y][x].set_neighbors(grid)
    queue = []
    path = []
    best_path = []
    cost = float("inf")

    # Setting basic
    begin_search = False
    searching = True
    start_point_set = False
    target_point_set = False
    target_point = None
    start_point = None
    g_score = {}

    BFS = False
    DIJKSTRA = False
    ASTAR = False
    BNB = False
    start_time = time.time()
    end_time = time.time()
    while True:
        for event in pygame.event.get():

            # Event Quit Window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Event control mouse
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Event click mouse left
                if event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    x = mouse_x // GAP
                    y = mouse_y // GAP
                    # While start_point has't been initialized yet
                    if not start_point_set and not grid[y][x].wall:
                        # Setting start point
                        start_point = grid[y][x]
                        start_point.start = True
                        start_point.visited = True
                        queue.append(start_point)
                        start_point_set = True
                # Event click mouse right
                elif event.button == 3:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    x = mouse_x // GAP
                    y = mouse_y // GAP
                    # While target_point has't been initialized
                    if not target_point_set and not grid[y][x].wall:
                        # Setting target point
                        if start_point != None:
                            if x == start_point.x and y == start_point.y:
                                continue
                        target_point = grid[y][x]

                        target_point.target = True
                        target_point_set = True

            elif event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Draw wall
                if event.buttons[0]:
                    x = mouse_x // GAP
                    y = mouse_y // GAP
                    if grid[y][x].start != True and grid[y][x].target != True:
                        grid[y][x].wall = True

            # Start algorithms
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c and target_point_set and start_point_set:
                    DIJKSTRA = True
                    is_printed = False
                    start_time = time.time()
                    if BNB or ASTAR:
                        BNB = False
                        ASTAR = False
                        start = start_point
                        target = target_point
                        queue = []
                        path = []
                        best_path = []
                        cost = float("inf")

                        # Setting basic
                        begin_search = False
                        searching = True
                        g_score = {}
                        for y in range(ROWS):
                            for x in range(COLS):
                                grid[y][x].visited = False
                                grid[y][x].prior = None
                                grid[y][x].queue = False
                        target_point = target
                        start_point = start
                    begin_search = True
                    queue = []
                    for y in range(ROWS):
                        for x in range(COLS):
                            g_score[(x, y)] = float("inf")
                    queue.append((0, start_point))
                    point = (start_point.x, start_point.y)
                    g_score[point] = 0
                elif event.key == pygame.K_a and target_point_set and start_point_set:
                    ASTAR = True
                    is_printed = False
                    start_time = time.time()
                    if BNB or DIJKSTRA:
                        BNB = False
                        DIJKSTRA = False
                        start = start_point
                        target = target_point
                        queue = []
                        path = []
                        best_path = []
                        cost = float("inf")

                        # Setting basic
                        begin_search = False
                        searching = True
                        g_score = {}
                        for y in range(ROWS):
                            for x in range(COLS):
                                grid[y][x].visited = False
                                grid[y][x].prior = None
                                grid[y][x].queue = False
                        target_point = target
                        start_point = start

                    begin_search = True
                    queue = []
                    for y in range(ROWS):
                        for x in range(COLS):
                            g_score[(x, y)] = float("inf")
                    queue.append((0, start_point))
                    point = (start_point.x, start_point.y)
                    g_score[point] = 0
                elif event.key == pygame.K_b and target_point_set and start_point_set:
                    BNB = True
                    is_printed = False
                    start_time = time.time()
                    if DIJKSTRA or ASTAR:
                        DIJKSTRA = False
                        ASTAR = False
                        start = start_point
                        target = target_point
                        queue = []
                        path = []
                        best_path = []
                        cost = float("inf")

                        # Setting basic
                        begin_search = False
                        searching = True
                        g_score = {}
                        for y in range(ROWS):
                            for x in range(COLS):
                                grid[y][x].visited = False
                                grid[y][x].prior = None
                                grid[y][x].queue = False
                        target_point = target
                        start_point = start

                    begin_search = True
                    queue = []
                    for y in range(ROWS):
                        for x in range(COLS):
                            g_score[(x, y)] = float("inf")

                    queue.append((heuristic(start_point, target_point), start_point))
                    point = (start_point.x, start_point.y)
                    g_score[point] = 0
                elif event.key == pygame.K_r:
                    DIJKSTRA = False
                    ASTAR = False
                    BNB = False
                    is_printed = False
                    queue = []
                    path = []
                    best_path = []
                    cost = float("inf")

                    # Setting basic
                    begin_search = False
                    searching = True
                    start_point_set = False
                    target_point_set = False
                    target_point = None
                    start_point = None
                    g_score = {}
                    for y in range(ROWS):
                        for x in range(COLS):
                            grid[y][x].set_default()
                elif event.key == pygame.K_m:
                    gen_maze(grid)
                    continue

        if begin_search:

            # While queue don't empty
            if len(queue) > 0 and searching:
                if ASTAR:
                    queue, path, searching, g_score = Search.a_star(
                        start_point,
                        target_point,
                        queue,
                        path,
                        searching,
                        g_score,
                        heuristic,
                    )
                    end_time = time.time()
                elif BNB:
                    if len(queue) > 0:
                        queue, path, searching, g_score, cost, best_path = Search.bnb(
                            start_point,
                            target_point,
                            queue,
                            path,
                            searching,
                            g_score,
                            heuristic,
                            cost,
                            best_path,
                        )
                    end_time = time.time()
                elif DIJKSTRA:
                    queue, path, searching, g_score = Search.dijkstra(
                        start_point, target_point, queue, path, searching, g_score
                    )
                    end_time = time.time()
            else:
                if searching:
                    if DIJKSTRA or ASTAR:
                        Tk().wm_withdraw()
                        messagebox.showinfo("No Solution", "There is no solution!")
                        searching = False
                    elif BNB:
                        path = best_path
                        searching = False
                        cur_point = path[-1]

                        while cur_point.prior != start_point:
                            path.append(cur_point.prior)
                            cur_point = cur_point.prior
                else:
                    if not is_printed:
                        print("Time: ", end_time - start_time)
                        is_printed = True
            sc.fill(BLACK)
        draw(grid, path)
        pygame.display.flip()
        clock.tick(144)


if __name__ == "__main__":
    main()
