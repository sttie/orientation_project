from figures import *

def area(p1, p2, p3):
    return (p2.x - p1.x) * (p3.y - p1.y) - (p2.y - p1.y) * (p3.x - p1.x)

def sub_intersect(x1, x2, x3, x4):
    if x1 > x2:
        x1, x2 = x2, x1
    if x3 > x4:
        x3, x4 = x4, x3
    
    return max(x1, x3) <= min(x2, x4)

# Функция проверяет отрезки на пересечение. Отрезки "на стыке" тоже считаются пересекающимися
def has_intersection(seg1, seg2):
    flag  = sub_intersect(seg1.start.x, seg1.end.x, seg2.start.x, seg2.end.x)
    flag &= sub_intersect(seg1.start.y, seg1.end.y, seg2.start.y, seg2.end.y)
    flag &= area(seg1.start, seg1.end, seg2.start) * area(seg1.start, seg1.end, seg2.end) <= 0
    flag &= area(seg2.start, seg2.end, seg1.start) * area(seg2.start, seg2.end, seg1.end) <= 0

    return flag


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
def check_segment_intersections(polygons, edge, count_intersections=False):
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
                intersections_amount += has_intersection(edge, segment)
                # Если нам неважно количество пересечений, просто заканчиваем цикл
                if intersections_amount == 1 and not count_intersections:
                    break

        if intersections_amount == 1 and not count_intersections:
            break

    return intersections_amount



def in_area(edge, polygons, radius):
    for polygon in polygons:
        for vertex in polygon:
            square_polygon = [Point(vertex.x - radius, vertex.y + radius), Point(vertex.x - radius, vertex.y - radius),
                            Point(vertex.x + radius, vertex.y + radius), Point(vertex.x + radius, vertex.y - radius)]

            if edge.start in square_polygon and edge.end in square_polygon:
                return 0

            if check_segment_intersections([square_polygon], edge):
                return 1

    return 0

"""
Основная функция. Строит граф видимости
polygons - список "псевдо полигонов" (т.е. полигонов, к которым добавились точки, отстоящие от вершин на какую-то величину)
polygons_to_not_intersect - исходные полигоны, которые были нарисованы пользователем
start_point - стартовая точка
end_point - конечная точка

Общие сведения по работе функции:
Чтобы оптимально (!) хранить граф, было принято решение сопоставить каждой вершине
определенное число, начиная с 0. Таким образом, можно хранить граф просто в виде матрицы смежности
и не тратить дополнительную память на хранение объектов типа Point в графе
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
    veiw_graph = Graph(vertex_amount)

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
            # Куча различных проверок на пересечения, но все отчасти понятно из названий функций
            if not in_area(new_edge, polygons_to_not_intersect, radius) and not check_if_segment_in_polygon(polygons, new_edge) \
                        and not check_segment_intersections(polygons_to_not_intersect, new_edge) \
                        and (new_edge in get_segments(polygons_to_not_intersect[sub_polygon]) \
                             or not check_if_segment_in_polygon(polygons_to_not_intersect, new_edge)):
                # вычисляем длину ребра
                weight = weight_evaluate(new_edge)
                # и добавляем его в граф видимости
                first_point_index, second_point_index = all_points.index(new_edge.start), all_points.index(new_edge.end)
                veiw_graph.add_edge((first_point_index, second_point_index), weight)
            
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

        if not in_area(edge_with_start, polygons_to_not_intersect, radius) and not check_segment_intersections(polygons_to_not_intersect, edge_with_start):
            weight = weight_evaluate(edge_with_start)
            second_point_index = all_points.index(edge_with_start.start)
            veiw_graph.add_edge((0, second_point_index), weight)

        if not in_area(edge_with_end, polygons_to_not_intersect, radius) and not check_segment_intersections(polygons_to_not_intersect, edge_with_end):
            weight = weight_evaluate(edge_with_end)
            second_point_index = all_points.index(edge_with_end.start)
            veiw_graph.add_edge((vertex_amount - 1, second_point_index), weight)

        p_idx += 1


    # Ребро между стартовой и конечной точками
    edge = Segment(start_point, end_point)
    if not in_area(edge, polygons_to_not_intersect, radius) and not check_segment_intersections(polygons_to_not_intersect, edge):
        weight = weight_evaluate(edge)
        veiw_graph.add_edge((0, vertex_amount - 1), weight)


    # Возвращаем граф видимости и непрерывный список всех точек
    return veiw_graph, all_points
