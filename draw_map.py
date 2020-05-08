import pygame
from figures import *
from intersections import check_point_in_polygon, build_view_graph
from geometry import pseudo_minkowski_sum, radius_okay
from astar import astar_algo
from dijkstra import dijkstra_algo


# Разные константы для читаемости
FPS = 24
fpsClock = pygame.time.Clock()
WIDTH = 1200
HEIGHT = 900
ROBOT_RADIUS = 10
END_POINT_RADIUS = 4
LEFT_BUTTON = 1
RIGHT_BUTTON = 3
WHITE = (255, 255, 255)
RED = (255, 0, 50)
BLACK = (0, 0, 0)
YELLOW = (225, 225, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
VIOLET = (139, 0, 255)


# Рисование полигона
def draw_polygon(display, polygon, line_colour=BLACK, circle_colour=RED, enough=False):
    if enough:
        polygon.append(polygon[0])

    for i in range(len(polygon) - 1):
        pygame.draw.aaline(display, line_colour, (polygon[i].x, polygon[i].y), (polygon[i+1].x, polygon[i+1].y))


# Отрисовка и обновление окна
def window_update(display, polygons, start_point, end_point):
    display.fill(WHITE)

    for polygon in polygons:
        draw_polygon(display, polygon)
    
    if not start_point is None:
        pygame.draw.circle(display, GREEN, (start_point.x, start_point.y), ROBOT_RADIUS)
    if not end_point is None:
        pygame.draw.circle(display, BLUE, (end_point.x, end_point.y), END_POINT_RADIUS)

    pygame.display.update()


def drawer_loop(display):
    # Список полигонов ДЛЯ ОТРИСОВКИ
    polygons = []
    # Список тех полигонов, относительно которых будет строится граф видимости
    polygons_to_check = []
    
    # Флаг цикла отрисовки экрана
    running = 1
    # Флаги для определения, что пользователь сейчас вводит: полигон, стартовую или конечную точку
    polygons_draw = 1
    vertex_from = 1
    vertex_to = 1
    # Объявляем стартовую и конечную точки
    start_point = None
    end_point = None


    current_polygon = 0
    polygons.append([])

    while running:
        # Ограничиваем частоту кадров
        fpsClock.tick(FPS)

        for event in pygame.event.get():
            # Если нажали на кнопку мыши
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == LEFT_BUTTON:
                    # mouse_position[0] = x, mouse_position[1] = y
                    mouse_position = pygame.mouse.get_pos()

                    # Если все еще рисуем полигоны
                    if polygons_draw and radius_okay(polygons, *mouse_position):
                        new_point = Point(*mouse_position)
                        polygons[current_polygon].append(new_point)

                    # Если рисуем стартовую точку
                    elif vertex_from and radius_okay(polygons, *mouse_position) and not check_point_in_polygon(polygons, Point(*mouse_position)):
                        start_point = Point(*mouse_position)

                    # Если рисуем конечную точку
                    elif vertex_to and radius_okay(polygons, *mouse_position) and not check_point_in_polygon(polygons, Point(*mouse_position)):
                        end_point = Point(*mouse_position)


            elif event.type == pygame.KEYDOWN:
                # Если нажата клавиша Q и мы все еще рисуем полигоны
                if event.key == pygame.K_q and polygons_draw:
                    draw_polygon(display, polygons[current_polygon], enough=True)

                    # Теперь добавим модифицированный полигон
                    pseudo_obstacle = pseudo_minkowski_sum(polygons[current_polygon], ROBOT_RADIUS + 6)
                    polygons_to_check.append(pseudo_obstacle)

                    polygons.append([])
                    current_polygon += 1

                # Если нажата клавиша Е
                elif event.key == pygame.K_e:
                    if polygons_draw:
                        # если нажата клавиша Е, но перед этим текущий полигон не был закончен, заканчиваем его
                        if len(polygons[current_polygon]) != 0:
                            draw_polygon(display, polygons[current_polygon], True)
                        # если полигон закочен, то удаляем последний пустой полигон (а точнее заготовленное для него место в списке)
                        else:
                            polygons.pop()
                        
                        polygons_draw = 0
                    
                    # Закончили со стартовой точкой - теперь рисуем конечную
                    elif vertex_from and not start_point is None:
                        vertex_from = 0

                    # Закончили с конечной точкой - заканчиваем цикл
                    elif vertex_to and not end_point is None:
                        vertex_to = 0
                        running = 0

        # Отрисовываем все необходимое и обновляем экран
        window_update(display, polygons, start_point, end_point)



    font = pygame.font.Font(None, 36)
    texts = [font.render("Visibility graph", 1, (0, 0, 0)), font.render("Dijkstra path", 1, (0, 0, 0)), font.render("A* path", 1, (0, 0, 0))]
    current_text = texts[1]

    view_graph, all_points = build_view_graph(polygons_to_check, polygons, start_point, end_point, ROBOT_RADIUS)
    path_astar, astar_visited = astar_algo(view_graph, 0, view_graph.vertex_amount - 1, all_points)
    path_dijkstra, dijkstra_visited = dijkstra_algo(view_graph, 0, view_graph.vertex_amount - 1, all_points)


    # Если пути между точками нет, путь просто не будет отображаться
    if len(path_astar) == 2 and not view_graph.get_weight(0, view_graph.vertex_amount - 1):
        path_astar = []
    if len(path_dijkstra) == 2 and not view_graph.get_weight(0, view_graph.vertex_amount - 1):
        path_dijkstra = []


    # Флаг. Если -1, то отрисовывается граф видимости, если 0, то путь по алгоритму Дейкстры, если 1, то путь по алгоритму А*
    # Флаг меняется по нажатию клавиши Z
    view_flag = 0
    # Флаг цикла отрисовки экрана
    running = 1

    while running:
        # Ограничение частоты кадров
        fpsClock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = 0
                elif event.key == pygame.K_z:
                    view_flag = view_flag + 1 if view_flag < 1 else -1
                    current_text = texts[view_flag + 1]


        display.fill(WHITE)

        # Отрисовка графа видимости
        if view_flag == -1:
            for point in range(view_graph.vertex_amount):
                for point_to_connect in range(view_graph.vertex_amount):
                    # Если ребро между point и point_to_connect существует
                    if view_graph.get_weight(point, point_to_connect):
                        p1, p2 = all_points[point], all_points[point_to_connect]
                        pygame.draw.line(display, YELLOW, (p1.x, p1.y), (p2.x, p2.y), 2)

        # Отрисовка пути по Дейкстре
        elif view_flag == 0:
            for point_idx in range(len(path_dijkstra) - 1):
                p1, p2 = path_dijkstra[point_idx], path_dijkstra[point_idx + 1]
                pygame.draw.line(display, VIOLET, (p1.x, p1.y), (p2.x, p2.y), 2)

            for v in dijkstra_visited:
                point = all_points[v]
                pygame.draw.circle(display, RED, (point.x, point.y), 3)

        # Отрисовка пути по А*
        elif view_flag == 1:
            for point_idx in range(len(path_astar) - 1):
                p1, p2 = path_astar[point_idx], path_astar[point_idx + 1]
                pygame.draw.line(display, VIOLET, (p1.x, p1.y), (p2.x, p2.y), 2)

            for v in astar_visited:
                point = all_points[v]
                pygame.draw.circle(display, RED, (point.x, point.y), 3)

        # Отрисовываем текст
        display.blit(current_text, (20, 20))

        # Рисуем исходные препятствия
        for polygon in polygons:
            draw_polygon(display, polygon)

        # Рисуем стартовую и конечную точки
        pygame.draw.circle(display, GREEN, (start_point.x, start_point.y), ROBOT_RADIUS)
        pygame.draw.circle(display, BLUE, (end_point.x, end_point.y), END_POINT_RADIUS)

        # Обновляем экран
        pygame.display.update()



def drawer_init():
    pygame.init()
    display = pygame.display.set_mode((WIDTH, HEIGHT))
    display.fill(WHITE)
    pygame.display.set_caption("Редактор карты")

    return display


if __name__ == "__main__":
    display = drawer_init()
    drawer_loop(display)
    pygame.quit()
