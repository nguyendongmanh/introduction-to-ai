class Search:
    def __init__(self) -> None:
        pass

    @staticmethod
    def a_star(start_point, target_point, queue, path, searching, g_score, heuristic):
        f_cur, cur_point = queue.pop(0)
        cur_point.visited = True
        if cur_point == target_point:
            searching = False
            while cur_point.prior != start_point:
                path.append(cur_point.prior)
                cur_point = cur_point.prior
        else:
            for neighbor in cur_point.neighbors:
                point_cur = (cur_point.x, cur_point.y)
                temp_gScore = g_score[point_cur] + 1
                point_neighbor = (neighbor.x, neighbor.y)
                if (
                    not neighbor.queue
                    and not neighbor.wall
                    and temp_gScore < g_score[point_neighbor]
                ):
                    g_score[point_neighbor] = temp_gScore
                    f_score = g_score[point_neighbor] + heuristic(
                        neighbor, target_point
                    )
                    queue.append((f_score, neighbor))
                    queue = sorted(queue, key=lambda x: x[0])
                    neighbor.queue = True
                    neighbor.prior = cur_point
        return queue, path, searching, g_score

    @staticmethod
    def bfs(start_point, target_point, queue, path, searching):
        cur_point = queue.pop(0)
        cur_point.visited = True
        if cur_point == target_point:
            searching = False
            while cur_point.prior != start_point:
                path.append(cur_point.prior)
                cur_point = cur_point.prior
        else:
            for neighbor in cur_point.neighbors:
                if not neighbor.queue and not neighbor.wall:
                    queue.append(neighbor)
                    neighbor.queue = True
                    neighbor.prior = cur_point

        return queue, path, searching

    @staticmethod
    def bnb(
        start_point,
        target_point,
        queue,
        path,
        searching,
        g_score,
        heuristic,
        cost,
        best_path,
    ):
        f_cur, cur_point = queue.pop(0)
        cur_point.visited = True
        if cur_point == target_point:
            point_cur = (cur_point.x, cur_point.y)
            if g_score[point_cur] <= cost:
                cost = g_score[point_cur]
                while cur_point.prior != start_point:
                    path.append(cur_point.prior)
                    cur_point = cur_point.prior
                best_path = path
                path = []
        else:
            if f_cur < cost:
                temp = []
                for neighbor in cur_point.neighbors:
                    point_cur = (cur_point.x, cur_point.y)
                    temp_gScore = g_score[point_cur] + 1
                    point_neighbor = (neighbor.x, neighbor.y)
                    if (
                        not neighbor.queue
                        and not neighbor.wall
                        and temp_gScore < g_score[point_neighbor]
                    ):
                        g_score[point_neighbor] = temp_gScore
                        f_score = g_score[point_neighbor] + heuristic(
                            neighbor, target_point
                        )
                        temp.append((f_score, neighbor))
                        neighbor.queue = True
                        neighbor.prior = cur_point
                temp = sorted(temp, key=lambda x: x[0])
                queue = temp + queue
        return queue, path, searching, g_score, cost, best_path
