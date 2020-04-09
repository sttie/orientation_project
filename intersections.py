import draw_map as dm
import pygame
from figures import *

"""
Если прямая переходит через точки (x1, y1) и (x2, y2), то
уравнение этой прямой -- (y - y1)/(y2 - y1) = (x - x1)/(x2 - x1)
Или же: y = (y2 - y1)/(x2 - x1)x - (x1y2 - x2y1)/(x2 - x1) 
"""
def get_straight_equation(seg):
    k = (seg.end.y - seg.start.y)/(seg.end.x - seg.start.x)
    b = (seg.start.x*seg.end.y - seg.end.x*seg.start.y)/(seg.end.x - seg.start.x)

    return -k, b

"""
Прямые пересекаются, если существует такой х, что:
x = (b2 - b1)/(k1 - k2)
"""
def are_crossed(seg1, seg2):
    k1, b1 = get_straight_equation(seg1)
    k2, b2 = get_straight_equation(seg2)
    x = (b2 - b1)/(k1 - k2)

    xleft = max(seg1.start.x, seg2.start.x)
    xright = min(seg1.end.x, seg1.end.x)

    return 1 if xleft <= x <= xright else 0


# display = dm.drawer_init()
# polygons = dm.drawer_loop(display)
# pygame.quit()

# p1, p2 = polygons

# seg1 = Segment(p1[0], p1[1])
# seg2 = Segment(p2[0], p2[1])

# print(are_crossed(seg1, seg2))