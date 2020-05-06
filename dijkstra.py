# Ширина окна - 1200, высота - 900 => максимальная (округленная) длина ребра - 1500
MAXLEN = 1500

def dijkstra_algo(graph, start, end, all_points):
    dijkstra_visited = []
    lengths = [MAXLEN] * graph.vertex_amount
    visited = [0] * graph.vertex_amount
    ancestors = [0] * graph.vertex_amount
    lengths[start] = 0

    for i in range(graph.vertex_amount):
        vert = None
        for j in range(graph.vertex_amount):
            if not visited[j] and (vert == None or lengths[j] < lengths[vert]):
                vert = j

        if vert == end:
            break

        visited[vert] = 1
        dijkstra_visited.append(vert)

        for e in range(graph.vertex_amount):
            if graph.get_weight(vert, e):
                if lengths[vert] + graph.get_weight(vert, e) < lengths[e]:
                    lengths[e] = lengths[vert] + graph.get_weight(vert, e)
                    ancestors[e] = vert

    return find_path(start, end, ancestors, all_points), dijkstra_visited


def find_path(start, end, ancestors, all_points):
    path = []
    vert = end
    while vert != start:
        path.append(all_points[vert])
        vert = ancestors[vert]

    path.append(all_points[start])

    return path[::-1]
