from intersections import check_point_in_polygon
from figures import Point

# Добавляем 4 доп. вершины к каждой из вершин полигона
def pseudo_minkowski_sum(polygon, radius):
    new_polygon = []

    for p in polygon:
        sub_points = [Point(p.x - radius, p.y + radius), Point(p.x - radius, p.y - radius),
                        Point(p.x + radius, p.y + radius), Point(p.x + radius, p.y - radius)]

        for sub in sub_points:
            if not check_point_in_polygon([polygon], Point(sub.x, sub.y - 5)) \
                    and not check_point_in_polygon([polygon], Point(sub.x, sub.y + 5)) \
                    and not check_point_in_polygon([polygon], Point(sub.x - 5, sub.y)) \
                    and not check_point_in_polygon([polygon], Point(sub.x + 5, sub.y)):
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
