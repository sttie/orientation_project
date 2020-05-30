from figures import *
import geometry
import pygame


def weight_evaluate(edge):
    x = edge.end.x - edge.start.x
    y = edge.end.y - edge.start.y

    return (x**2 + y**2)**(1/2)


def get_intersection(seg1, seg2):
    start1, start2, end1, end2 = seg1.start, seg2.start, seg1.end, seg2.end

    dir1 = end1 - start1
    dir2 = end2 - start2

    a1 = -dir1.y
    b1 = dir1.x
    d1 = -(a1*start1.x + b1*start1.y)

    a2 = -dir2.y
    b2 = dir2.x
    d2 = -(a2*start2.x + b2*start2.y)

    # подставляем концы отрезков для выяснения в каких полуплоскоcтях они
    seg1_line2_start = a2*start1.x + b2*start1.y + d2
    seg1_line2_end = a2*end1.x + b2*end1.y + d2

    seg2_line1_start = a1*start2.x + b1*start2.y + d1
    seg2_line1_end = a1*end2.x + b1*end2.y + d1

    # если концы одного отрезка имеют один знак, значит он в одной полуплоскости и пересечения нет.
    if seg1_line2_start * seg1_line2_end >= 0 or seg2_line1_start * seg2_line1_end >= 0:
        return 0

    u = seg1_line2_start / (seg1_line2_start - seg1_line2_end)
    point = start1 + Point(u*dir1.x, u*dir1.y)

    return point


def circle_intersection(robot, radius, polygon, display):
    p0 = Point(robot.x - radius, robot.y + radius)
    p1 = Point(robot.x - radius, robot.y - radius)
    p2 = Point(robot.x + radius, robot.y - radius)
    p3 = Point(robot.x + radius, robot.y + radius)
    circle_polygon = [Segment(p0, p1), Segment(p1, p2), Segment(p2, p3), Segment(p3, p0)]

    for seg in polygon:
        if intersect([circle_polygon], seg, get_segs=False)[0]:
            return 1

    return 0


def check_square_intersections(robot, radius, polygon2):
    p0 = Point(robot.x - radius, robot.y + radius)
    p1 = Point(robot.x - radius, robot.y - radius)
    p2 = Point(robot.x + radius, robot.y - radius)
    p3 = Point(robot.x + radius, robot.y + radius)
    square = [Segment(p0, p1), Segment(p1, p2), Segment(p2, p3), Segment(p3, p0)]

    for seg1 in square:
        for seg2 in polygon2:
            if get_intersection(seg1, seg2):
                return 1

    return 0

"""
Проверка на то, принадлежит ли точка полигону
Возвращает 1, если да, 0 иначе
"""
def check_point_in_polygon(polygons, point, get_segs=True):
    y_point = point.y
    # Дабы избежать пересечений с просто точками, делаем координату дробной (т.к. все остальные координаты целые)
    if y_point == round(y_point):
        y_point += 0.5
    
    ray = Segment(point, Point(0, y_point))
    return intersect(polygons, ray, count_intersections=True, get_segs=get_segs)[0] % 2

"""
Проверка на то, находится ли отрезок в полигоне
Возвращает 1, если да, 0 иначе
"""
def check_if_segment_in_polygon(polygons, segment, get_segs=True):
    for polygon in polygons:
        if get_segs:
            segs = get_segments(polygon)
        else:
            segs = polygon
            
        if segment in segs or segment.reverse() in segs:
            return 0

    y_point = (segment.start.y + segment.end.y) / 2
    # Дабы избежать пересечений с просто точками, делаем координату дробной (т.к. все остальные координаты целые)
    if y_point == round(y_point):
        y_point += 0.5
    
    segment_center_point = Point((segment.start.x + segment.end.x) / 2, y_point)
    ray = Segment(segment_center_point, Point(0, y_point))
    
    return intersect(polygons, ray, count_intersections=True, get_segs=get_segs)[0] % 2


# Извлекает из полигона список его отрезков
def get_segments(polygon):
    segments = []

    for point_idx in range(len(polygon) - 1):
        segments.append(Segment(polygon[point_idx], polygon[point_idx + 1]))
    segments.append(Segment(polygon[-1], polygon[0]))

    return segments


"""
Функция проходится по всем ребрам всех полигонов и определяет,
есть ли пересечение new_edge с одним из рёбер.
polygons - список полигонов
edge - очередное ребро между двумя вершинами полигонов
count_intersections - если True, то нужно посчитать количество пересечений
intersections_amount - количество пересечений
"""
def intersect(polygons, edge, count_intersections=False, get_segs=True):
    points = []
    intersections_amount = 0
    
    # проверяем все отрезки всех полигонов
    for polygon in polygons:
        if get_segs:
            segments = get_segments(polygon)
        else:
            segments = polygon

        # Проверяем все отрезки
        for segment in segments:
            # Если отрезки не на стыке
            if not edge[0] in [segment[0], segment[1]] and not edge[1] in [segment[0], segment[1]]:
                # Пересечение есть => добавляем его к общему количеству
                point = get_intersection(edge, segment)
                if point:
                    points.append(point)
                    intersections_amount += 1
                # Если нам неважно количество пересечений, просто заканчиваем цикл
                if intersections_amount == 1 and not count_intersections:
                    break

        if intersections_amount == 1 and not count_intersections:
            break

    return intersections_amount, points


def check_if_polygons_in_polygon(polygons, outer_polygon, get_segs=True):
    for polygon in polygons:
        if get_segs:
            pol = get_segments(polygon)
        else:
            pol = polygon

        for segment in pol:
            if check_if_segment_in_polygon([outer_polygon], segment, get_segs=get_segs):
                return 1

    return 0


def check_strip(polygons, edge, radius):
    x1, x2, y1, y2, x3, x4, y3, y4 = geometry.get_rectangle(edge.start, edge.end, radius)
    # Эквивалентные представления одного полигона
    segs = [Segment(Point(x4, y4), Point(x3, y3)), Segment(Point(x3, y3), Point(x1, y1)), 
                Segment(Point(x1, y1), Point(x2, y2)), Segment(Point(x2, y2), Point(x4, y4))]

    for segment in segs:
        if intersect(polygons, segment)[0]:
            return 1
    
    # Для исключения полигонов, которые меньше полосы робота
    if check_if_polygons_in_polygon(polygons, segs, get_segs=False):
        return 1

    return 0


def count_intersections(square, polygon):
    inters = [0, 0, 0, 0]

    for seg in polygon:
        if get_intersection(square[0], seg):
            inters[0] += 1
        if get_intersection(square[1], seg):
            inters[1] += 1
        if get_intersection(square[2], seg):
            inters[2] += 1
        if get_intersection(square[3], seg):
            inters[3] += 1

    return inters



def build_view_graph(polygons, polygons_to_not_intersect, radius):
    polygon_idx = 0
    polygons_amount = len(polygons)
    all_points = []

    while polygon_idx < polygons_amount:
        point_idx = 0

        while point_idx < len(polygons[polygon_idx]) - 1:
            all_points.append(polygons[polygon_idx][point_idx])
            point_idx += 1

        polygon_idx += 1

    # Количество всех точек
    vertex_amount = len(all_points)
    # Создаем сам граф видимости
    view_graph = Graph(vertex_amount)
    # Индекс текущей точки
    p_idx = 0
    # cur_polygon - индекс текущего полигона
    cur_polygon = 0

    # Проходимся по всем полигонам
    while cur_polygon < polygons_amount and p_idx <= len(polygons[cur_polygon]) - 1:
        # Если все точки в текущем полигоне проверены, переходим к следующему полигону (причем последняя точка каждого полигона совпадает с его первой точкой)
        if p_idx == len(polygons[cur_polygon]) - 1:
            cur_polygon += 1
            p_idx = 0
            continue
        
        # Для i-ой точки проверяем все i+1-ые точки, начиная с текущего полигона
        an_p_idx = p_idx + 1
        sub_polygon = cur_polygon
        while sub_polygon < polygons_amount and an_p_idx <= len(polygons[sub_polygon]) - 1:
            if an_p_idx == len(polygons[sub_polygon]) - 1:
                sub_polygon += 1
                an_p_idx = 0
                continue

            # Cтроим ребро между текущей парой точек
            new_edge = Segment(polygons[cur_polygon][p_idx], polygons[sub_polygon][an_p_idx])
            # Если текущее ребро не находится целиком в полигоне И заметаемая полоса не пересекает никакие полигоны, то можно добавлять текущее ребро в граф
            
            if not check_if_segment_in_polygon(polygons_to_not_intersect, new_edge) and not check_strip(polygons_to_not_intersect, new_edge, radius):
                # вычисляем длину ребра
                weight = weight_evaluate(new_edge)
                # и добавляем его в граф видимости
                first_point_index, second_point_index = all_points.index(new_edge.start), all_points.index(new_edge.end)
                view_graph.add_edge((first_point_index, second_point_index), weight)
            
            # Переходим к следующей паре точек
            an_p_idx += 1

        # Переходим к следующей точке
        p_idx += 1


    # Возвращаем граф видимости и непрерывный список всех точек
    return view_graph, all_points


#! TODO: какая-то ошибка с несоответствием двух списков полигонов
def add_points(view_graph, all_points, polygons, polygons_to_not_intersect, radius, start, end):
    all_points.append(start)
    all_points.append(end)
    view_graph.update_amount()

    polygons_amount = len(polygons)
    vertex_amount = view_graph.vertex_amount

    # Ребро между стартовой и конечной точками
    edge = Segment(start, end)
    if not check_strip(polygons_to_not_intersect, edge, radius):
        weight = weight_evaluate(edge)
        view_graph.add_edge((vertex_amount - 2, vertex_amount - 1), weight)

    # Можно закончить перебор досрочно
    if view_graph.get_weight(vertex_amount - 2, vertex_amount - 1):
        return view_graph, all_points


    p_idx = 0
    cur_polygon = 0

    while cur_polygon < polygons_amount and p_idx <= len(polygons[cur_polygon]) - 1:
        if p_idx == len(polygons[cur_polygon]) - 1:
            cur_polygon += 1
            p_idx = 0
            continue

        edge_with_start = Segment(polygons[cur_polygon][p_idx], start)
        edge_with_end = Segment(polygons[cur_polygon][p_idx], end)

        if not check_strip(polygons_to_not_intersect, edge_with_start, radius):
            weight = weight_evaluate(edge_with_start)
            second_point_index = all_points.index(edge_with_start.start)
            view_graph.add_edge((vertex_amount - 2, second_point_index), weight)

        if not check_strip(polygons_to_not_intersect, edge_with_end, radius):
            weight = weight_evaluate(edge_with_end)
            second_point_index = all_points.index(edge_with_end.start)
            view_graph.add_edge((vertex_amount - 1, second_point_index), weight)

        p_idx += 1

    
    return view_graph, all_points