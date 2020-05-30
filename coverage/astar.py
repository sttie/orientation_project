from heapq import heappush as push, heappop as pop

# Эвристическая оценка h(v) - евклидово расстояние от точки v до конечной
def heuristics(v, end):
    return ((v.x - end.x)**2 + (v.y - end.y)**2)**(1/2)


"""
В процессе работы рассчитывается функция f(v) = g(v) + h(v), где
g(v) - наименьшая стоимость пути в v из start_point
h(v) - эвристическое приближение стоимости пути от v до end_point
Открытые алгоритмом вершины хранятся в очереди с приоритетом по значению f(v)
"""
def astar_algo(graph, start, end, all_points):
    to_visit = []
    ancestors = [0] * graph.vertex_amount
    lengths = [0] * graph.vertex_amount
    visited = [0] * graph.vertex_amount

    push(to_visit, (0, start))
    lengths[start] = 0

    while len(to_visit) > 0:
        current_vert = pop(to_visit)[1]

        if visited[current_vert]:
            continue

        if current_vert == end:
            break

        for neighbor in graph.matrix[current_vert]:
            neighbor_num, weight = neighbor[0], neighbor[1]
            cost = lengths[current_vert] + weight
            if not lengths[neighbor_num] or cost < lengths[neighbor_num]:
                lengths[neighbor_num] = cost
                prior = cost + heuristics(all_points[neighbor_num], all_points[end])
                push(to_visit, (prior, neighbor_num))
                ancestors[neighbor_num] = current_vert

        visited[current_vert] = 1

    return find_path(start, end, ancestors, all_points)


def find_path(start, end, ancestors, all_points):
    path = []
    vert = end
    while vert != start:
        path.append(all_points[vert])
        vert = ancestors[vert]

    path.append(all_points[start])

    return path[::-1]
