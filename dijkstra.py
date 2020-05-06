from heapq import heappush as push, heappop as pop

# Ширина окна - 1200, высота - 900 => максимальная (округленная) длина ребра - 1500
MAXLEN = 1500

def find_path(start, end, ancestors, all_points):
    path = []
    vert = end
    while vert != start:
        path.append(all_points[vert])
        vert = ancestors[vert]

    path.append(all_points[start])

    return path[::-1]


def dijkstra_algo(graph, start, end, all_points):
    dijkstra_visited = []
    to_visit = []
    lengths = [0] * graph.vertex_amount
    ancestors = [0] * graph.vertex_amount
    
    push(to_visit, (0, start))
    lengths[start] = 0

    while len(to_visit) > 0:
        current_vert = pop(to_visit)[1]

        if current_vert == end:
            break

        dijkstra_visited.append(current_vert)

        for neighbor in range(graph.vertex_amount):
            if not graph.get_weight(current_vert, neighbor):
                continue

            cost = lengths[current_vert] + graph.get_weight(current_vert, neighbor)
            if not lengths[neighbor] or cost < lengths[neighbor]:
                lengths[neighbor] = cost
                push(to_visit, (cost, neighbor))
                ancestors[neighbor] = current_vert

    return find_path(start, end, ancestors, all_points), dijkstra_visited
