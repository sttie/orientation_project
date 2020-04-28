from copy import copy

def radius_okay(polygons, x, y, RADIUS=11):
    okay = 1

    for polygon in polygons:
        if not okay:
            break

        for point in polygon:
            if not okay:
                break
            if (x - point.x)**2 + (y - point.y)**2 <= RADIUS**2:
                okay = 0

    return okay

"""
Сумма Минковского двух отрезков (по сути, четырех точек)
center отнимается только один раз для того, чтобы построенная 
сумма Минковского сразу строилась относительно изначального начала отсчета системы координат
"""
def two_segments_MS(start1, end1, start2, end2, center):
    answer = []

    # векторная сумма всех пар точек
    answer.append(start1 + end2 - center)
    answer.append(start1 + start2 - center)
    answer.append(end1 + start2 - center)
    answer.append(end1 + end2 - center)

    return answer


# Сумма Минковского двух полигонов
def minkowski_sum(polygon1, polygon2, center):
    ans = []
    
    i = 0
    while i < len(polygon1) - 1:
        j = 0
        while j < len(polygon2) - 1:
            ans += two_segments_MS(polygon1[i], polygon1[i+1], polygon2[j], polygon2[j+1], center)
            j += 1

        i += 1

    return ans


# Функция возвращает 1, если точка c находится справа от ab
def right_rotate(a, b, c):
    return a.x * (b.y - c.y) + b.x * (c.y - a.y) + c.x * (a.y - b.y) < 0


# Функция возвращает все "впадины" невыпуклых полигонов
def detect_nonconvex_points(poly):
    polygon = copy(poly)
    point_idx = 0
    nonconvex_points = []
    left_point = polygon[0]

    # ищем самую левую нижнюю точку
    for i in range(1, len(polygon)):
        if polygon[i].x < left_point.x:
            polygon[i], left_point = left_point, polygon[i]


    while point_idx < len(polygon) - 1:
        if right_rotate(polygon[point_idx-1], polygon[point_idx], polygon[point_idx+1]):
            nonconvex_points.append(polygon[point_idx])

        point_idx += 1


    return nonconvex_points


# Вычисление минимальной выпуклой оболочки (метод Грэхэма, O(nlogn))
def make_convex_hull(polygon):
    n = len(polygon)
    p_indexes = [i for i in range(n)]

    # Ищем самую левую самую нижнюю точку
    for i in range(1, n):
        if polygon[p_indexes[i]].x < polygon[p_indexes[0]].x:
            p_indexes[i], p_indexes[0] = p_indexes[0], p_indexes[i]

    # Сортируем все точки по углу
    for i in range(2, n):
        j = i
        while j > 1 and right_rotate(polygon[p_indexes[0]], polygon[p_indexes[j-1]], polygon[p_indexes[j]]):
            p_indexes[j], p_indexes[j-1] = p_indexes[j-1], p_indexes[j]
            j -= 1

    # "Стек" для того, чтобы убирать "впадины". В нем находятся индексы точек из polygon
    stack = [p_indexes[0], p_indexes[1]]

    for i in range(2, n):
        # Если поворот НЕ правый, то точка нам не подходит, удаляем ее
        while right_rotate(polygon[stack[-2]], polygon[stack[-1]], polygon[p_indexes[i]]):
            stack.pop(-1)
        stack.append(p_indexes[i])

    # Суем это все в результат
    result = []
    for idx in stack:
        result.append(polygon[idx])
    # Замыкаем полигон
    result.append(result[0])

    return result
