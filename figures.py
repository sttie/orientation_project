class Graph:
    def __init__(self, vertex_amount):
        self.vertex_amount = vertex_amount
        self.matrix = []
        for i in range(vertex_amount):
            self.matrix.append([0] * vertex_amount)

    # Добавление ребра edge = (vertex1, vertex2) с весом weight
    def add_edge(self, edge, weight):
        vertex1, vertex2 = edge

        self.matrix[vertex1][vertex2] = weight
        self.matrix[vertex2][vertex1] = weight

    def get_weight(self, vertex1, vertex2):
        return self.matrix[vertex1][vertex2]


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __str__(self):
        return "({}, {})".format(self.x, self.y)

    def __hash__(self):
        return self.x.__hash__() ^ self.y.__hash__()


class Segment:
    def __init__(self, start, end):
        # start, end - объекты класса Point
        self.start = start
        self.end = end
    
    def __eq__(self, another):
        return self.start == another.start and self.end == another.end or self.end == another.start and self.start == another.end

    def __getitem__(self, key):
        if not key in [0, 1]:
            raise IndexError
        
        return self.start if key == 0 else self.end

    def __str__(self):
        return "[{}, {}]".format(self.start, self.end)


class Polygon:
    def __init__(self, points=[]):
        self.points = points

    def add_point_xy(self, x, y):
        self.points.append(Point(x, y))

    def add_point_p(self, point):
        self.points.append(point)

    def index(self, obj):
        return self.points.index(obj)

    def inp(self, point):
        return point in self.points

    def __getitem__(self, key):
        return self.points[key]

    def __len__(self):
        return len(self.points)
    
    def __iter__(self):
        for point in self.points:
            yield point
