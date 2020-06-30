from figures import *
import geometry



def has_intersection(seg1, seg2):
    x1, x2, y1, y2 = seg1.start.x, seg1.end.x, seg1.start.y, seg1.end.y    
    x3, x4, y3, y4 = seg2.start.x, seg2.end.x, seg2.start.y, seg2.end.y  

    znam = (y4-y3)*(x2-x1) - (x4-x3)*(y2-y1)
    if znam == 0:
        return 1 if seg1 == seg2 else 0

    ua = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / znam
    ub = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)) / znam

    if not (0 <= ua <= 1 and 0 <= ub <= 1):
        return 0

    x = x1 + ua*(x2 - x1)
    y = y1 + ub*(y2 - y1)

    return (x, y)


"""
Проверка на то, принадлежит ли точка полигону
Возвращает 1, если да, 0 иначе
"""
def check_point_in_polygon(polygons, point):
    y_point = point.y
    # Дабы избежать пересечений с просто точками, делаем координату дробной (т.к. все остальные координаты целые)
    if y_point == round(y_point):
        y_point += 0.5
    
    ray = Segment(point, Point(0, y_point))
    return check_segment_intersections(polygons, ray, count_intersections=True) % 2

"""
Проверка на то, находится ли отрезок в полигоне
Возвращает 1, если да, 0 иначе
"""
def check_if_segment_in_polygon(polygons, segment):
    y_point = (segment.start.y + segment.end.y) / 2
    # Дабы избежать пересечений с просто точками, делаем координату дробной (т.к. все остальные координаты целые)
    if y_point == round(y_point):
        y_point += 0.5
    
    segment_center_point = Point((segment.start.x + segment.end.x) / 2, y_point)
    ray = Segment(segment_center_point, Point(0, y_point))
    
    return check_segment_intersections(polygons, ray, count_intersections=True) % 2


# Извлекает из полигона список его отрезков
def get_segments(polygon):
    segments = []

    for point_idx in range(len(polygon) - 1):
        segments.append(Segment(polygon[point_idx], polygon[point_idx + 1]))

    return segments


# Вычисление длины ребра
def weight_evaluate(edge):
    x = edge.end.x - edge.start.x
    y = edge.end.y - edge.start.y

    return (x**2 + y**2)**(1/2)


"""
Функция проходится по всем ребрам всех полигонов и определяет,
есть ли пересечение new_edge с одним из рёбер.
polygons - список полигонов
edge - очередное ребро между двумя вершинами полигонов
count_intersections - если True, то нужно посчитать количество пересечений
intersections_amount - количество пересечений
"""
def check_segment_intersections(polygons, edge, count_intersections=False, sub_polygon=None):
    intersections_amount = 0
    
    # проверяем все отрезки всех полигонов
    for polygon in polygons:
        # Переводим список вершин к списку отрезков
        segments = get_segments(polygon)
        # Проверяем все отрезки
        for segment in segments:
            # Если отрезки не на стыке
            if not edge[0] in [segment[0], segment[1]] and not edge[1] in [segment[0], segment[1]]:
                # Пересечение есть => добавляем его к общему количеству
                if has_intersection(edge, segment):
                    intersections_amount += 1
                    
                # Если нам неважно количество пересечений, просто заканчиваем цикл
                if intersections_amount == 1 and not count_intersections:
                    break

        if intersections_amount == 1 and not count_intersections:
            break

    return intersections_amount


def check_if_polygons_in_polygon(polygons, outer_polygon):
    for polygon in polygons:
        for segment in get_segments(polygon):
            if check_if_segment_in_polygon([outer_polygon], segment):
                return 1

    return 0


def check_strip(polygons, edge, radius):
    x1, x2, y1, y2, x3, x4, y3, y4 = geometry.get_rectangle(edge.start, edge.end, radius)
    # Эквивалентные представления одного полигона
    segs = [Segment(Point(x4, y4), Point(x3, y3)), Segment(Point(x3, y3), Point(x1, y1)), 
                Segment(Point(x1, y1), Point(x2, y2)), Segment(Point(x2, y2), Point(x4, y4))]
    strip_polygon = [Point(x4, y4), Point(x3, y3), Point(x1, y1), Point(x2, y2), Point(x4, y4)]


    for segment in segs:
        if check_segment_intersections(polygons, segment):
            return 1
    
    # Для исключения полигонов, которые меньше полосы робота
    if check_if_polygons_in_polygon(polygons, strip_polygon):
        return 1

    return 0


"""
Основная функция. Строит граф видимости
polygons - список "псевдо полигонов" (т.е. полигонов, к которым добавились точки, отстоящие от вершин на какой-то радиус)
polygons_to_not_intersect - исходные полигоны, которые были нарисованы пользователем
start_point - стартовая точка
end_point - конечная точка
"""
def build_view_graph(polygons, polygons_to_not_intersect, start_point, end_point, radius):
    polygon_idx = 0
    polygons_amount = len(polygons)

    # Добавляем все точки в непрерывный список точек (причем стартовая точка - самая первая)
    all_points = [start_point]
    while polygon_idx < polygons_amount:
        point_idx = 0

        while point_idx < len(polygons[polygon_idx]) - 1:
            all_points.append(polygons[polygon_idx][point_idx])
            point_idx += 1

        polygon_idx += 1
    # А также добавляем последнюю точку
    all_points.append(end_point)

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

            # написать функцию которая НЕ строит ребро между точкой и точкой если она входит в отстоящие вон те точки

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


    # Здесь все абсолютно то же самое, только строятся ребра отдельно от стартовой и конечной точек
    p_idx = 0
    cur_polygon = 0

    while cur_polygon < polygons_amount and p_idx <= len(polygons[cur_polygon]) - 1:
        if p_idx == len(polygons[cur_polygon]) - 1:
            cur_polygon += 1
            p_idx = 0
            continue

        edge_with_start = Segment(polygons[cur_polygon][p_idx], start_point)
        edge_with_end = Segment(polygons[cur_polygon][p_idx], end_point)

        if not check_strip(polygons_to_not_intersect, edge_with_start, radius):
            weight = weight_evaluate(edge_with_start)
            second_point_index = all_points.index(edge_with_start.start)
            view_graph.add_edge((0, second_point_index), weight)

        if not check_strip(polygons_to_not_intersect, edge_with_end, radius):
            weight = weight_evaluate(edge_with_end)
            second_point_index = all_points.index(edge_with_end.start)
            view_graph.add_edge((vertex_amount - 1, second_point_index), weight)

        p_idx += 1


    # Ребро между стартовой и конечной точками
    edge = Segment(start_point, end_point)
    if not check_strip(polygons_to_not_intersect, edge, radius):
        weight = weight_evaluate(edge)
        view_graph.add_edge((0, vertex_amount - 1), weight)


    # Возвращаем граф видимости и непрерывный список всех точек
    return view_graph, all_points
