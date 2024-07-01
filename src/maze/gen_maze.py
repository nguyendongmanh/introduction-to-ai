from global_settings import ROWS, COLS
import random


def break_wall(current, new, grid):
    if current.x == new.x:
        if current.y > new.y:
            grid[current.y - 1][current.x].wall = False
        else:
            grid[current.y + 1][current.x].wall = False
    else:
        if current.x > new.x:
            grid[current.y][current.x - 1].wall = False
        else:
            grid[current.y][current.x + 1].wall = False


def get_neighbors(cell, grid):
    neighbors = []
    x, y = cell.x, cell.y
    if x > 1:
        neighbors.append(grid[y][x - 2])
    if x < COLS - 2:
        neighbors.append(grid[y][x + 2])
    if y > 1:
        neighbors.append(grid[y - 2][x])
    if y < ROWS - 2:
        neighbors.append(grid[y + 2][x])
    return neighbors


def gen_maze(grid, start_x: int = -1, start_y: int = -1):
    # Đặt tất cả các ô thành tường
    for y in range(ROWS):
        for x in range(COLS):
            grid[y][x].wall = True

    # Chọn ngẫu nhiên một ô bắt đầu
    if start_x == -1:
        start_x = random.randint(0, (COLS // 2) - 1) * 2

    if start_y == -1:
        start_y = random.randint(0, (ROWS // 2) - 1) * 2
    start = grid[start_y][start_x]
    start.wall = False

    in_maze = {start}
    remaining_cells = {
        grid[y][x] for y in range(0, ROWS, 2) for x in range(0, COLS, 2)
    } - in_maze

    while remaining_cells:
        # Chọn ngẫu nhiên một ô còn lại để bắt đầu đường đi ngẫu nhiên
        walk_start = random.choice(list(remaining_cells))
        path = [walk_start]

        while path[-1] not in in_maze:
            current = path[-1]
            neighbors = get_neighbors(current, grid)
            next_cell = random.choice(neighbors)
            if next_cell in path:
                # Nếu ô đã nằm trong đường đi, xóa vòng lặp
                path = path[: path.index(next_cell) + 1]
            else:
                path.append(next_cell)

        # Thêm đường đi vào mê cung
        for i in range(len(path) - 1):
            break_wall(path[i], path[i + 1], grid)
            path[i].wall = False
            in_maze.add(path[i])
            remaining_cells.discard(path[i])

        in_maze.add(path[-1])
        remaining_cells.discard(path[-1])
