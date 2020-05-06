from figures import Point
import intersections

# Сложно в комментариях объяснить все эти формулы
# Функция берет две точки и строит прямоугольник с одной из сторон, равной radius,
# с этими точками по центру двух противоположных сторон
def get_rectangle(point, point2, radius):
    x1, x2, y1, y2 = point.x, point2.x, point.y, point2.y
    
    # Если координаты по иксу равны, то с точностью можно сказать об игриках
    if x1 == x2:
        x3_1 = radius + x2
        x3_2 = -radius + x2
        x4_1 = radius + x1
        x4_2 = -radius + x1

        y4_1 = y4_2 = y1
        y3_1 = y3_2 = y2
    
    else:
        seg_len = ((x2 - x1)**2 + (y2 - y1)**2) ** (1/2)

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


    return x4_1, x4_2, y4_1, y4_2, x3_1, x3_2, y3_1, y3_2


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
