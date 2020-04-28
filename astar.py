# Ширина окна - 1000, высота - 700 => максимальная (округленная) длина ребра - 1221
MAXLEN = 1221

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

    def is_in(self, element):
        for v in self.queue:
            if v[0] == element:
                return 1
        
        return 0
    
    def pop_value(self, value):
        for i in range(self.size):
            if self.queue[i][0] == value:
                self.queue.pop(i)


"""
Эвристическая оценка h(v) - евклидово расстояние от текущей точки до конечной
"""
def heuristics(v, end):
    return ((v.x - end.x)**2 + (v.y - end.y)**2)**(1/2)

"""
В процессе работы рассчитывается функция f(v) = g(v) + h(v), где
g(v) - наименьшая стоимость пути в v из start_point
h(v) - эвристическое приближение стоимости пути от v до end_point
Открытые алгоритмом вершины можно хранить в очереди с приоритетом по значению f(v)
# visited - Q, lengths_from_start - g, target_func - f
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


# def astar_algo(graph, start, end, all_points):
#     to_visit = PriorityQueue()
#     to_visit.push(start, 0)
#     visited = [0] * graph.vertex_amount
#     lengths_from_start = [0] * graph.vertex_amount
#     ancestors = [0] * graph.vertex_amount

#     to_visit.push(start, 0)
#     lengths_from_start[start] = 0

#     while not to_visit.is_empty():
#         current_vert = to_visit.pop_front()[0]
#         # нужно ли оставить? поменяется ли кратчайший путь?
#         if current_vert == end:
#             break
        
#         visited[current_vert] = 1

#         # range(graph.vertex_amount) можно заменить graph.get_neighbours(current_vert)
#         for v in range(graph.vertex_amount):
#             # нет смысла проверять не смежные с current_vert вершины
#             if graph.matrix[current_vert][v] == 0:
#                 continue

#             cost = lengths_from_start[current_vert] + graph.get_weight(current_vert, v)

#             # ВСЕ МЕНЯЕТ NOT VISITED[V] - ДОЛЖНО БЫТЬ NOT lengths_from_start[v]

#             # Если v уже была посещена и текущая оценка >=, то пропускаем ее
#             if visited[v] and cost >= lengths_from_start[v]:
#                 continue
#             if not visited[v] or cost < lengths_from_start[v]:
#                 ancestors[v] = current_vert
#                 lengths_from_start[v] = cost
#                 priority = lengths_from_start[v] + heuristics(all_points[v], all_points[end])
#                 if not to_visit.is_in(v):
#                     to_visit.push(v, priority)

#     return find_path(start, end, ancestors, all_points)


def find_path(start, end, ancestors, all_points):
    path = []
    vert = end
    while vert != start:
        path.append(all_points[vert])
        vert = ancestors[vert]

    path.append(all_points[start])

    return path[::-1]


