from figures import Point, Segment
from geometry import find_polygon
import intersections


def is_on_seg(seg, point):
    x, y = point.x, point.y
    x1, y1, x2, y2 = seg.start.x, seg.start.y, seg.end.x, seg.end.y

    return (x - x2)/(x1 - x2) == (y - y2)/(y1 - y2)


def find_polygon(polygons, point):
    p1 = Point(point.x, point.y - 1)
    p2 = Point(point.x, point.y + 2)
    seg2 = Segment(p1, p2)

    for polygon in polygons:
        segs = intersections.get_segments(polygon)
        for seg in segs:
            if intersections.get_intersection(seg, seg2):
                return polygon


# Сложно в комментариях объяснить все эти формулы
# Функция берет две точки и строит прямоугольник с одной из сторон, равной radius,
# с этими точками по центру двух противоположных сторон
def get_rectangle(point, point2, radius):
    x1, x2, y1, y2 = point.x, point2.x, point.y, point2.y

    seg_len = ((x2 - x1)**2 + (y2 - y1)**2) ** (1/2)

    if x1 == x2:
        x3_1 = radius + x2
        x3_2 = -radius + x2
        x4_1 = radius + x1
        x4_2 = -radius + x1

        y4_1 = y4_2 = y1
        y3_1 = y3_2 = y2
    
    else:
        # Считаем для x4, y4
        suby1 = (radius * (x2 - x1)) / seg_len
        k1 = (suby1 * (y2 - y1)) / (x2 - x1)

        y4_1 = -suby1 + y1
        y4_2 = suby1 + y1
        x4_1 = k1 + x1
        x4_2 = -k1 + x1


        # Считаем для x3, y3
        suby2 = (radius * (x2 - x1)) / seg_len
        k2 = (suby2 * (y2 - y1)) / (x2 - x1)

        y3_1 = -suby1 + y2
        y3_2 = suby1 + y2
        x3_1 = k2 + x2
        x3_2 = -k2 + x2


    # теперь нужно немного "удлинить" прямоугольник
    # Point(x4_1, y4_1) и Point(x4_2, y4_2) находятся с одной стороны
    x1, x2, y1, y2 = x4_1, x4_2, y4_1, y4_2
    seg_len = ((x2 - x1)**2 + (y2 - y1)**2) ** (1/2)

    if x1 == x2:
        if point.x < point2.x:
            x4 = x1 - radius
            x3 = x2 - radius
        else:
            x4 = x1 + radius
            x3 = x2 + radius
        y4 = y1
        y3 = y2
    
    else:
        sub = (radius * (x2 - x1)) / seg_len
        k = (-sub * (y2 - y1)) / (x2 - x1)

        y3 = sub + y2
        x3 = k + x2
        y4 = sub + y1
        x4 = k + x1
    
    
    x1, x2, y1, y2 = x3_1, x3_2, y3_1, y3_2
    seg_len = ((x2 - x1)**2 + (y2 - y1)**2) ** (1/2)

    if x1 == x2:
        if point.x < point2.x:
            x6 = x2 + radius
            x5 = x1 + radius
        else:
            x6 = x2 - radius
            x5 = x1 - radius

        y5 = y2
        y6 = y1

    else:
        sub = -(radius * (x2 - x1)) / seg_len
        k = (-sub * (y2 - y1)) / (x2 - x1)

        y5 = sub + y2
        x5 = k + x2
        y6 = sub + y1
        x6 = k + x1

    if x3 == x5:
        x3 -= radius
        x4 += radius
        x5 -= radius
        x6 += radius

    return x3, x4, y3, y4, x5, x6, y5, y6


# Эти формулы тоже сложжно просто так объяснить, выводил в тетради
def pseudo_minkowski_sum(polygon, radius):
    new_polygon = []

    for p in polygon:
        x0, y0 = p.x, p.y
        x1, x5 = x0 - radius, x0 + radius
        a2 = radius**2 * (2 - 2**(1/2))
        x2 = int((a2 - x1**2 - radius**2 + x0**2) / (2*(x0 - x1)))
        x3 = int((a2 - x5**2 - radius**2 + x0**2) / (2*(x0 - x5)))
        y2 = int(((a2**(1/2) * (4*radius**2 - a2)**(1/2)) / (2*radius))) + y0
        y3 = -int(((a2**(1/2) * (4*radius**2 - a2)**(1/2)) / (2*radius))) + y0

        # Список точек, образующих правильный восьмиугольник
        sub_points = [Point(x0 - radius, y0), Point(x2, y3), Point(x0, y0 - radius), Point(x3, y3), 
                        Point(x0 + radius, y0), Point(x3, y2), Point(x0, y0 + radius), Point(x2, y2)]

        # Также проверяем точки на принадлежность полигону, чтобы немного ускорить построение графа видимости
        for sub_point in sub_points:
            if not intersections.check_point_in_polygon([polygon], sub_point):
                new_polygon.append(sub_point)

    return new_polygon


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
