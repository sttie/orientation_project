import pygame
import figures

# FPS?

WIDTH = 1000
HEIGHT = 700
LEFT_BUTTON = 1
RIGHT_BUTTON = 3
WHITE = (255, 255, 255)
RED = (255, 0, 50)
BLACK = (0, 0, 0)


def draw_polygon(display, polygon, enough=False):
    # if enough and len(polygon) <= 2:
    #     print("INVALID POLYGON")
    #     exit(0)
    if enough:
        polygon.add_point_p(polygon[0])


    for i in range(len(polygon) - 1):
        pygame.draw.aaline(display, BLACK, (polygon[i].x, polygon[i].y), (polygon[i+1].x, polygon[i+1].y))
        pygame.draw.circle(display, RED, (polygon[i].x, polygon[i].y), 5)
        pygame.draw.circle(display, RED, (polygon[i+1].x, polygon[i+1].y), 5)


def window_update(display, polygons):
    pygame.display.update()
    for polygon in polygons:
        draw_polygon(display, polygon, False)


def drawer_loop(display):
    polygons = []
    running = 1
    current_polygon = 0
    polygons.append(figures.Polygon([]))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == LEFT_BUTTON:
                    mouse_position = pygame.mouse.get_pos()
                    new_point = figures.Point(mouse_position[0], mouse_position[1])
                    polygons[current_polygon].add_point_p(new_point)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    draw_polygon(display, polygons[current_polygon], True)
                    polygons.append(figures.Polygon([]))
                    current_polygon += 1

                elif event.key == pygame.K_e:
                    if len(polygons[current_polygon]) != 0:
                        draw_polygon(display, polygons[current_polygon], True)
                    else:
                        polygons.pop()

                    running = 0

        window_update(display, polygons)

    return polygons


def drawer_init():
    pygame.init()
    display = pygame.display.set_mode((WIDTH, HEIGHT))
    display.fill(WHITE)
    pygame.display.set_caption("Рисование карты")

    return display


if __name__ == "__main__":
    display = drawer_init()
    polygons = drawer_loop(display)
    pygame.quit()