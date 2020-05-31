import pygame
from figures import Point, Segment
from astar import astar_algo
from intersections import *


def draw_seg(display, seg, color, width=4):
    pygame.draw.line(display, color, (seg.start.x, seg.start.y), (seg.end.x, seg.end.y), width)
    pygame.display.update()
    pass


def make_polygon_from_cell(cell):
    polygon = []
    polygon.append(cell.left_border)

    for ceiling in cell.ceiling_edges:
        polygon.append(ceiling)

    polygon.append(cell.right_border)

    for floor in cell.floor_edges[::-1]:
        polygon.append(floor)

    return polygon


def move_on_path(path, display, fpsClock):
    point_index = 0
    speed = 5
    robot = path[0]

    while point_index < len(path) - 1:
        p1, p2 = path[point_index], path[point_index + 1]
        seg = Segment(Point(p1.x, p1.y), Point(p2.x, p2.y))
        length = ((p2.x - p1.x)**2 + (p2.y - p1.y)**2)**(1/2)

        parts = int(length / speed)

        if seg.end.y > seg.start.y:
            dir_y = 1
        else:
            dir_y = -1
        if seg.end.x > seg.start.x:
            dir_x = 1
        else:
            dir_x = -1

        draw_seg(display, seg, (255, 0, 0))

        for i in range(parts):
            fpsClock.tick(50)
            x = (max(seg.end.x, seg.start.x) - min(seg.end.x, seg.start.x)) / parts
            y = (max(seg.end.y, seg.start.y) - min(seg.end.y, seg.start.y)) / parts
            robot.x += dir_x * x
            robot.y += dir_y * y
            
            pygame.draw.circle(display, (0, 255, 0), (int(robot.x), int(robot.y)), 12)
            pygame.display.update()
            pygame.draw.circle(display, (0, 0, 255), (int(robot.x), int(robot.y)), 12)


        point_index += 1


def eval_condition(robot, polygon, radius):
    p0 = Point(robot.x - radius, robot.y + radius)
    p1 = Point(robot.x - radius, robot.y - radius)
    p2 = Point(robot.x + radius, robot.y - radius)
    p3 = Point(robot.x + radius, robot.y + radius)
    square = [Segment(p0, p1), Segment(p1, p2), Segment(p2, p3), Segment(p3, p0)]

    inters = count_intersections(square, polygon)
    # Нулевой случай, если нет пересечений
    condition = 0

    if inters in [[0, 1, 1, 0], [1, 1, 0, 0], [0, 2, 0, 0], 
                  [0, 1, 0, 0], [1, 2, 1, 0]]:
        condition = 1
    
    elif inters in [[0, 0, 1, 1], [1, 0, 0, 1], [0, 0, 0, 2],
                    [0, 0, 0, 1], [1, 0, 1, 2], [0, 0, 1, 0], [1, 0, 0, 0]]:
        condition = 2

    # 3 и 4 случаи
    elif inters == [1, 0, 1, 0]:
        # Необходимо проверить, препятствие сверху или снизу
        # Для этого "поднимаем" робота на радиус и проверяем, осталось ли пересечение
        robot.y -= radius + 1

        if check_square_intersections(robot, radius, polygon):
            condition = 1
        else:
            condition = 2

        robot.y += radius + 1

    # Вариации 5 и 6 случаев
    if inters == [1, 1, 1, 1]:
        pass

    return condition, inters


def cover_new_cell(cells, current_cell, robot, radius, view_graph, all_points, pseudo_polygons, polygons, display, fpsClock):
# Если дошли до правой границы, переходим к следующей клетке
    path = None
    while path is None or len(path) == 2 and not view_graph.get_weight(view_graph.vertex_amount - 2, view_graph.vertex_amount - 1):
        cell = cells[current_cell]
        polygon = make_polygon_from_cell(cell)
        
        condition = eval_condition(robot, polygon, radius)[0]
        while condition:
            if condition == 1:
                robot.y += radius - 1
                if not circle_intersection(robot, radius, polygon, display):
                    robot.x += radius // 2
                if circle_intersection(robot, radius, polygon, display):
                    robot.y += radius

            elif condition == 2:
                robot.y -= radius - 1
                if not circle_intersection(robot, radius, polygon, display):
                    robot.x += radius // 2
                if circle_intersection(robot, radius, polygon, display):
                    robot.y -= radius

            if condition == 13:
                pass

            pygame.draw.circle(display, (0, 255, 0), (int(robot.x), int(robot.y)), radius)
            pygame.display.update()
            pygame.draw.circle(display, (0, 0, 255), (int(robot.x), int(robot.y)), radius)
            condition = eval_condition(robot, polygon, radius)[0]
        

        current_cell += 1
        if current_cell == len(cells):
            break
                    
        cell = cells[current_cell]
        polygon = make_polygon_from_cell(cell)
        end = cell.left_border.end + radius + 1

        # Сдвигаем точку туда, куда робот сможет встать
        inters = eval_condition(end, polygon, radius)[1]
        while sum(inters):
            end.y += radius // 2
            inters = eval_condition(end, polygon, radius)[1]


        # Если не нашлось подходящего места, то клетка слишком мала и ее нужно пропустить
        if not check_point_in_polygon([polygon], end, get_segs=False):
            continue

        view_graph, all_points = add_points(view_graph, all_points, pseudo_polygons, polygons, radius + 1, robot, end)                    
        path = astar_algo(view_graph, view_graph.vertex_amount - 2, view_graph.vertex_amount - 1, all_points)

        if path is not None and (len(path) != 2 or view_graph.get_weight(view_graph.vertex_amount - 2, view_graph.vertex_amount - 1)):                    
            move_on_path(path, display, fpsClock)

            while circle_intersection(robot, radius, polygon, display):
                robot.y += radius // 2

    if path is None or len(path) == 2 and not view_graph.get_weight(view_graph.vertex_amount - 2, view_graph.vertex_amount - 1):
        print("Нет ни одной доступной клетки")

    return current_cell


def start_coverage(cells, view_graph, all_points, polygons, pseudo_polygons, radius, display, fpsClock):
    robot = Point(radius + 1, radius)
    current_cell = 0

    while current_cell < len(cells):
        cell = cells[current_cell]
        polygon = make_polygon_from_cell(cell)
        direction = 1

        while not circle_intersection(robot, radius, polygon, display) or robot.x + radius >= cell.right_border.start.x:
            fpsClock.tick(65)

            if robot.x + radius >= cell.right_border.start.x:
                current_cell = cover_new_cell(cells, current_cell, robot, radius, view_graph, all_points, pseudo_polygons, polygons, display, fpsClock)
                break

            robot.y += direction * (radius // 2 - 1)       
            pygame.draw.circle(display, (0, 255, 0), (int(robot.x), int(robot.y - 2*direction)), radius)
            pygame.display.update()
            pygame.draw.circle(display, (0, 0, 255), (int(robot.x), int(robot.y - 2*direction)), radius)

            condition, inters = eval_condition(robot, polygon, radius)  
            prev_inters = []       
            while condition:
                if inters in prev_inters:                        
                    current_cell = cover_new_cell(cells, current_cell, robot, radius, view_graph, all_points, pseudo_polygons, polygons, display, fpsClock)
                    cell = cells[current_cell]
                    polygon = make_polygon_from_cell(cell)
                    break

                if condition == 1:
                    robot.y += radius - 1
                    direction = 1
                    if not circle_intersection(robot, radius, polygon, display):
                        robot.x += radius // 2
                    if circle_intersection(robot, radius, polygon, display):
                        robot.y += radius

                elif condition == 2:
                    robot.y -= radius - 1
                    direction = -1
                    if not circle_intersection(robot, radius, polygon, display):
                        robot.x += radius // 2
                    if circle_intersection(robot, radius, polygon, display):
                        robot.y -= radius

                if condition == 13:
                    pass

                pygame.draw.circle(display, (0, 255, 0), (int(robot.x), int(robot.y - 2*direction)), radius)
                pygame.display.update()
                pygame.draw.circle(display, (0, 0, 255), (int(robot.x), int(robot.y - 2*direction)), radius)
                condition, inters = eval_condition(robot, polygon, radius)
                if inters != [0, 0, 0, 0]:
                    prev_inters.append(inters)
