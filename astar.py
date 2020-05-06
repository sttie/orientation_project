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
    astar_visited = []
    to_visit = []
    push(to_visit, (0, start))
    ancestors = [0] * graph.vertex_amount
    lengths = [0] * graph.vertex_amount
    lengths[start] = 0

    while len(to_visit) > 0:
        current_vert = pop(to_visit)[1]

        if current_vert == end:
            break

        astar_visited.append(current_vert)

        for v in range(graph.vertex_amount):
            if not graph.get_weight(current_vert, v):
                continue

            cost = lengths[current_vert] + graph.get_weight(current_vert, v)
            if not lengths[v] or cost < lengths[v]:
                lengths[v] = cost
                prior = cost + heuristics(all_points[v], all_points[end])
                push(to_visit, (prior, v))
                ancestors[v] = current_vert

    return find_path(start, end, ancestors, all_points), astar_visited


def find_path(start, end, ancestors, all_points):
    path = []
    vert = end
    while vert != start:
        path.append(all_points[vert])
        vert = ancestors[vert]

    path.append(all_points[start])

    return path[::-1]
