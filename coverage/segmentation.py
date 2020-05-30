from intersections import *
from operator import attrgetter
from figures import Segment, Point
import math
import pygame


class Cell:
    def __init__(self, ceiling_edges, floor_edges, left_border, right_border):
        self.ceiling_edges = ceiling_edges
        self.floor_edges = floor_edges
        self.left_border = left_border
        self.right_border = right_border
        self.cleaned = 0

class Event:
    def __init__(self, event_type, location, floor, ceiling):
        self.event_type = event_type
        self.location = location
        self.floor = floor
        self.ceiling = ceiling

IN = 0
FLOOR = 1
CEILING = 2
OUT = 3
        

def sort_polygons(polygons):
    new_polygons = []
    for polygon in polygons:
        polygon.pop(-1)

        new = []
        leftmost = Point(1001, 1001)
        index = 0
        for i in range(len(polygon)):
            if polygon[i].x < leftmost.x:
                leftmost = polygon[i]
                index = i
        new.append(leftmost)

        next_idx = None
        if index == len(polygon) - 1:
            p1, p2 = polygon[index-1], polygon[0]
        else:
            p1, p2 = polygon[index-1], polygon[index+1]

        if p1.y > p2.y:
            if p1.x < p2.x:
                next_idx = 0 if index == len(polygon) - 1 else index + 1
                direction = 1
            else:
                next_idx = index - 1
                direction = -1
        else:
            next_idx = 0 if index == len(polygon) - 1 else index + 1
            direction = 1

        next_point = polygon[next_idx]
        new.append(next_point)

        if direction == 1:
            for i in range(next_idx + 1, len(polygon)):
                new.append(polygon[i])
            if index != len(polygon) - 1:
                for i in range(index):
                    new.append(polygon[i])
        else:
            for i in range(next_idx - 1, -1, -1):
                new.append(polygon[i])
            for i in range(len(polygon) - 1, index, -1):
                new.append(polygon[i])


        new_polygons.append(new)

    return new_polygons


def is_polygon(polygon):
    flag = 1

    for i in range(len(polygon) - 1):
        if polygon[i].end != polygon[i+1].start:
            flag = 0
            break
    
    if flag and polygon[-1].end != polygon[0].start:
        flag = 0

    return flag


# Поиск первого пересечения
def get_min_intersection(polygons, seg, direction):
    points = intersect(polygons, seg, count_intersections=True)[1]
    if len(points) == 0:
        return None

    if direction == 1:
        return min(points, key=lambda p: p.y)
    else:
        return max(points, key=lambda p: p.y)


def get_current_cell(cells, event_pos, carriage, polygons, display):
    sorted_cells = cells.copy()
    # начнем обход клеток справа (так быстрее дойдем до нужной)
    sorted_cells.sort(key=lambda e: e.left_border.start.x, reverse=True)

    for cell in sorted_cells:
        polygon = [cell.left_border]

        for seg in cell.ceiling_edges[:-1]:
            polygon.append(seg)

        last_ceiling = Segment(cell.ceiling_edges[-1].start, carriage.start)

        if intersect(polygons, last_ceiling.round())[0]:
            continue
        
        polygon.append(last_ceiling)

        # добавляем новую каретку
        polygon.append(carriage)

        first_floor = Segment(carriage.end, cell.floor_edges[-1].start)
        polygon.append(first_floor)

        if intersect(polygons, first_floor.round())[0]:
            continue

        # добавляем нижнюю часть полигона
        for seg in cell.floor_edges[::-1][1:]:
            polygon.append(seg.reverse())
    
        # проверяем, является ли это полигоном
        if is_polygon(polygon) or check_if_polygons_in_polygon(polygons, polygon, get_segs=False):
            return cell


def map_segmentation(polygons_old, map_width, map_height, display):
    events = []
    polygons = polygons_old.copy()
    polygons = sort_polygons(polygons)


    for polygon in polygons:
        rightmost = Point(-1, -1)
        leftmost = Point(1001, 1001)
        for i in range(len(polygon)):
            if rightmost.x < polygon[i].x:
                rightmost = polygon[i]
            if leftmost.x > polygon[i].x:
                leftmost = polygon[i]

        # Создаем новое событие IN
        ceiling_pointer = Segment(leftmost, polygon[1])
        events.append(Event(IN, leftmost, None, ceiling_pointer))
        index = 1

        in_pos = len(events) - 1

        # Добавляем все точки вплоть до крайней справа в качестве CEILING
        while polygon[index] != rightmost:
            ceiling_pointer = Segment(polygon[index], polygon[index + 1])
            events.append(Event(CEILING, polygon[index], None, ceiling_pointer))
            index += 1

        # Нашли крайнюю справа точку - добавили событие OUT
        floor_pointer = None
        if index + 1 < len(polygon):
            floor_pointer = Segment(rightmost, polygon[index + 1])
        ceiling_pointer = Segment(polygon[index - 1], rightmost)
        events.append(Event(OUT, rightmost, floor_pointer, ceiling_pointer))
        index += 1

        # Добавляем ВСЕ оставшиеся точки в качестве событий FLOOR...
        while index < len(polygon):
            floor_pointer = Segment(polygon[index - 1], polygon[index])
            events.append(Event(FLOOR, polygon[index], floor_pointer, None))
            index += 1

        # ... плюс последнее ребро
        floor_pointer = Segment(polygon[-1], leftmost)
        events[in_pos].floor = floor_pointer

    # Сортируем события по координате по иксу и событию
    events.sort(key=attrgetter("location.x", "event_type"))
    

    cells = []
    current_cells = []

    # Правые границы будут определяться потом
    first_cell = Cell([Segment(Point(0, 0), None)], [Segment(Point(0, map_height), None)], Segment(Point(0, map_height), Point(0, 0)), None)
    current_cells.append(first_cell)

    event_idx = 0
    while event_idx < len(events):
        event = events[event_idx]
        event_pos = event.location
        carriage_up = Segment(Point(event_pos.x, 0), Point(event_pos.x, event_pos.y-0.5))
        carriage_down = Segment(Point(event_pos.x, event_pos.y+0.5), Point(event_pos.x, map_height))
        # None, если часть каретка пересекается только с границей карты
        c = get_min_intersection(polygons, carriage_up, 0)
        f = get_min_intersection(polygons, carriage_down, 1)

        if event.event_type == IN:
            carriage = None
            # Инициализируем каретки в зависимости от пересечений
            if c is None and f is None:
                carriage = Segment(Point(event_pos.x, 0), Point(event_pos.x, map_height))
            elif c is not None and f is not None:
                carriage = Segment(c, f)
            elif c is None and f is not None:
                carriage = Segment(Point(event_pos.x, 0), f)
            elif c is not None and f is None:
                carriage = Segment(c, Point(event_pos.x, map_height))

            current_cell = get_current_cell(current_cells, event_pos, carriage, polygons, display)

            # Заканчиваем последние отрезки
            if f is None and c is None:
                current_cell.ceiling_edges[-1].end = Point(event_pos.x, 0)
                current_cell.floor_edges[-1].end = Point(event_pos.x, map_height)
            elif f is None and c is not None:
                current_cell.ceiling_edges[-1].end = c
                current_cell.floor_edges[-1].end = Point(event_pos.x, map_height)
            elif f is not None and c is None:
                current_cell.ceiling_edges[-1].end = Point(event_pos.x, 0)
                current_cell.floor_edges[-1].end = f
            if c is not None and f is not None:
                current_cell.ceiling_edges[-1].end = c
                current_cell.floor_edges[-1].end = f


            current_cell.right_border = carriage.reverse()


            # Здесь имеем полную информацию о последней клетке => можно ее добавить в список
            cells.append(current_cell)
            # Текущая клетка уже обработана => можно ее удалить из списка
            if events[event_idx + 1].event_type != IN or events[event_idx + 1].location.x != event_pos.x:
                current_cells.remove(current_cell)

            # Открываем нижнюю и верхнюю клетки
            bottom_cell = Cell([], [], None, None)
            top_cell = Cell([], [], None, None)
            
            # Инициализируем некоторые поля новосозданных клеток
            if c is None:
                top_cell.left_border = Segment(event_pos, Point(event_pos.x, 0))
                top_ceiling = Segment(Point(event_pos.x, 0), None)
            else:
                top_cell.left_border = Segment(event_pos, c)
                top_ceiling = Segment(c, None)


            top_floor = Segment(event.floor.end, None)
            top_cell.floor_edges.append(top_floor)
            top_cell.ceiling_edges.append(top_ceiling)


            if f is None:
                bottom_cell.left_border = Segment(Point(event_pos.x, map_height), event_pos)
                bottom_floor = Segment(Point(event_pos.x, map_height), None)
            else:
                bottom_cell.left_border = Segment(f, event_pos)
                bottom_floor = Segment(f, None)
            
            bottom_ceiling = Segment(event.ceiling.start, None)
            bottom_cell.floor_edges.append(bottom_floor)
            bottom_cell.ceiling_edges.append(bottom_ceiling)

            # Добавляем новые клетки в список обрабатывающихся клеток
            current_cells.append(top_cell)
            current_cells.append(bottom_cell)


        # Определяем текущую клетку, в нее добавляем соответствующие отрезки
        elif event.event_type == FLOOR:
            # точка "с" сверху => делаем каретку, помня об этом
            carriage = None
            if c is None:
                carriage = Segment(Point(event_pos.x, 0), event_pos)
            else:
                carriage = Segment(c, event_pos)

            current_cell = get_current_cell(current_cells, event_pos, carriage, polygons, display)
            current_cell.floor_edges[-1].end = event.floor.end
            current_cell.floor_edges.append(Segment(event.floor.end, None))


        elif event.event_type == CEILING:
            # точка "f" снизу => делаем каретку, помня об этом
            carriage = None
            if f is None:
                carriage = Segment(event_pos, Point(event_pos.x, map_height))
            else:
                carriage = Segment(event_pos, f)

            current_cell = get_current_cell(current_cells, event_pos, carriage, polygons, display)
            current_cell.ceiling_edges[-1].end = event.ceiling.start
            current_cell.ceiling_edges.append(Segment(event.ceiling.start, None))


        elif event.event_type == OUT:
            carriage_top = None
            carriage_bottom = None
            if c is None:
                carriage_top = Segment(Point(event_pos.x, 0), event_pos)
            else:
                carriage_top = Segment(c, event_pos)
            if f is None:
                carriage_bottom = Segment(event_pos, Point(event_pos.x, map_height))
            else:
                carriage_bottom = Segment(event_pos, f)


            current_bottom_cell = get_current_cell(current_cells, event_pos, carriage_bottom, polygons, display)
            # Эта клетка была задействована => сразу удаляем ее
            current_cells.remove(current_bottom_cell)
            # И здесь так же
            current_top_cell = get_current_cell(current_cells, event_pos, carriage_top, polygons, display)
            current_cells.remove(current_top_cell)

            current_bottom_cell.right_border = carriage_bottom
            current_top_cell.right_border = carriage_top

            current_bottom_cell.floor_edges[-1].end = carriage_bottom.end
            current_bottom_cell.ceiling_edges[-1].end = carriage_bottom.start

            current_top_cell.floor_edges[-1].end = carriage_top.end
            current_top_cell.ceiling_edges[-1].end = carriage_top.start


            cells.append(current_top_cell)
            cells.append(current_bottom_cell)

            # Создаем новую клетку
            # Левая граница теперь снизу вверх
            new_cell_carriage = Segment(carriage_bottom.end, carriage_top.start)
            new_cell = Cell([Segment(new_cell_carriage.end, None)], [Segment(new_cell_carriage.start, None)], new_cell_carriage, None)
            current_cells.append(new_cell)

        event_idx += 1


    # Последняя клетка
    last_cell = current_cells[-1]
    carriage = Segment(Point(map_width, 0), Point(map_width, map_height))
    last_cell.ceiling_edges[-1].end = Point(map_width, 0)
    last_cell.floor_edges[-1].end = Point(map_width, map_height)
    last_cell.right_border = carriage
    cells.append(last_cell)        

    return cells
