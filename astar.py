# Очередь с приоритетом
class PriorityQueue:
    def __init__(self):
        self.queue = []
        self.size = 0

    def push(self, value, weight):
        idx = 0
        while idx < self.size and self.queue[idx][1] <= weight:
            idx += 1

        if idx == self.size:
            self.queue.append((value, weight))
        else:
            self.queue.insert(idx, (value, weight))

        self.size += 1

    def pop_front(self):
        self.size -= 1
        return self.queue.pop(0)
    
    def is_empty(self):
        return self.size == 0


"""
Эвристическая оценка h(v) - евклидово расстояние от точки v до конечной
"""
def heuristics(v, end):
    return ((v.x - end.x)**2 + (v.y - end.y)**2)**(1/2)

"""
В процессе работы рассчитывается функция f(v) = g(v) + h(v), где
g(v) - наименьшая стоимость пути в v из start_point
h(v) - эвристическое приближение стоимости пути от v до end_point
Открытые алгоритмом вершины хранятся в очереди с приоритетом по значению f(v)
"""
def astar_algo(graph, start, end, all_points):
    to_visit = PriorityQueue()
    to_visit.push(start, 0)
    ancestors = [0] * graph.vertex_amount
    lengths = [0] * graph.vertex_amount
    lengths[start] = 0

    while not to_visit.is_empty():
        current_vert = to_visit.pop_front()[0]
        if current_vert == end:
            break

        for v in range(graph.vertex_amount):
            if graph.matrix[current_vert][v] == 0:
                continue

            cost = lengths[current_vert] + graph.get_weight(current_vert, v)
            if not lengths[v] or cost < lengths[v]:
                lengths[v] = cost
                prior = cost + heuristics(all_points[v], all_points[end])
                to_visit.push(v, prior)
                ancestors[v] = current_vert

    return find_path(start, end, ancestors, all_points)


def find_path(start, end, ancestors, all_points):
    path = []
    vert = end
    while vert != start:
        path.append(all_points[vert])
        vert = ancestors[vert]

    path.append(all_points[start])

    return path[::-1]


