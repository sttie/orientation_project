import pygame
from figures import *
import geometry
import segmentation as segm
import coverage as cov
from intersections import build_view_graph
from astar import astar_algo


# Разные константы для читаемости
FPS = 60
fpsClock = pygame.time.Clock()
WIDTH = 600
HEIGHT = 600
ROBOT_RADIUS = 11
LEFT_BUTTON = 1
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
        pygame.draw.line(display, line_colour, (polygon[i].x, polygon[i].y), (polygon[i+1].x, polygon[i+1].y), 2)


def dump(polygons):
    dumpfile = open("dump.txt", "w")
    for i in range(len(polygons)):
        for point in polygons[i]:
            dumpfile.write(str(point))
            dumpfile.write("\n")

        dumpfile.write("\n")


def drawer_loop(display):
    # Список полигонов
    polygons = []
    pseudo_polygons = []
    # Флаг цикла отрисовки экрана
    running = 1
    current_polygon = 0

    polygons.append([])


    while running:
        # Ограничиваем частоту кадров
        fpsClock.tick(FPS)

        for event in pygame.event.get():
            # Если нажали на кнопку мыши
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == LEFT_BUTTON:
                    # mouse_position[0] = x, mouse_position[1] = y
                    mouse_position = pygame.mouse.get_pos()
                    new_point = Point(*mouse_position)
                    polygons[current_polygon].append(new_point)


            elif event.type == pygame.KEYDOWN:
                # Если нажата клавиша Q и мы все еще рисуем полигоны
                if event.key == pygame.K_q:
                    draw_polygon(display, polygons[current_polygon], enough=True)

                    pseudo_obstacle = geometry.pseudo_minkowski_sum(polygons[current_polygon], ROBOT_RADIUS + 8)
                    pseudo_polygons.append(pseudo_obstacle)

                    polygons.append([])
                    current_polygon += 1

                # Если нажата клавиша Е
                elif event.key == pygame.K_e:
                    running = 0

        # Отрисовываем все необходимое и обновляем экран
        display.fill(WHITE)

        for polygon in polygons:
            draw_polygon(display, polygon)

        pygame.display.update()


    # ==============================================================
    polygons.pop(-1)
    view_graph, all_points = build_view_graph(pseudo_polygons, polygons, ROBOT_RADIUS + 1)
    dump(polygons)

    # Сегментация карты
    cells = segm.map_segmentation(polygons, WIDTH, HEIGHT, display)    
    # Начало обхода
    cov.start_coverage(cells, view_graph, all_points, polygons, pseudo_polygons, ROBOT_RADIUS, display, fpsClock)

    running = 1
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                running = 0


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