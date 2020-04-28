# Ширина окна - 1000, высота - 700 => максимальная (округленная) длина ребра - 1221
MAXLEN = 1221

def find_path(start, end, ancestors, all_points):
    path = []
    vert = end
    while vert != start:
        path.append(all_points[vert])
        vert = ancestors[vert]

    path.append(all_points[start])

    return path[::-1]


def dijkstra_algo(graph, start, end, all_points):
    # setdefault 0, setdefault MAXLEN
    lengths = [MAXLEN] * graph.vertex_amount
    visited = [0] * graph.vertex_amount
    ancestors = [0] * graph.vertex_amount
    lengths[start] = 0

    for i in range(graph.vertex_amount):
        vert = None
        for j in range(graph.vertex_amount):
            if not visited[j] and (vert == None or lengths[j] < lengths[vert]):
                vert = j

        if lengths[vert] == MAXLEN:
            break

        visited[vert] = 1
        for e in range(graph.vertex_amount):
            # если ребро между vert и e существует
            if graph.get_weight(vert, e) != 0:
                if lengths[vert] + graph.get_weight(vert, e) < lengths[e]:
                    lengths[e] = lengths[vert] + graph.get_weight(vert, e)
                    ancestors[e] = vert

    return find_path(start, end, ancestors, all_points)