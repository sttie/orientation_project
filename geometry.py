from figures import Point


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


def pseudo_minkowski_sum(polygon, radius):
    new_polygon = []

    for p in polygon:
        sub_points = [Point(p.x - radius, p.y - radius), Point(p.x + radius, p.y - radius),
                        Point(p.x + radius, p.y + radius), Point(p.x - radius, p.y + radius), Point(p.x - radius, p.y - radius)]

        for sub in sub_points:
            new_polygon.append(sub)

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
