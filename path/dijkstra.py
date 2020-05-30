from heapq import heappush as push, heappop as pop


def dijkstra_algo(graph, start, end, all_points):
    dijkstra_visited = []
    to_visit = []
    lengths = [0] * graph.vertex_amount
    ancestors = [0] * graph.vertex_amount
    visited = [0] * graph.vertex_amount
    
    push(to_visit, (0, start))
    lengths[start] = 0

    while len(to_visit) > 0:
        current_vert = pop(to_visit)[1]

        if visited[current_vert]:
            continue

        if current_vert == end:
            break

        dijkstra_visited.append(current_vert)

        # Проходимся по соседям current_vert
        for neighbor in graph.matrix[current_vert]:
            neighbor_num, weight = neighbor[0], neighbor[1]
            cost = lengths[current_vert] + weight
            if not lengths[neighbor_num] or cost < lengths[neighbor_num]:
                lengths[neighbor_num] = cost
                push(to_visit, (cost, neighbor_num))
                ancestors[neighbor_num] = current_vert

        visited[current_vert] = 1

    return find_path(start, end, ancestors, all_points), dijkstra_visited


def find_path(start, end, ancestors, all_points):
    path = []
    vert = end
    while vert != start:
        path.append(all_points[vert])
        vert = ancestors[vert]

    path.append(all_points[start])

    return path[::-1]