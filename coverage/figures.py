class Graph:
    def __init__(self, vertex_amount):
        self.vertex_amount = vertex_amount
        self.matrix = []
        for i in range(vertex_amount):
            self.matrix.append([])

    # Добавление ребра edge = (vertex1, vertex2) с весом weight
    def add_edge(self, edge, weight):
        vertex1, vertex2 = edge

        self.matrix[vertex1].append((vertex2, weight))
        self.matrix[vertex2].append((vertex1, weight))

    # Ищем нужное ребро, не нашли => возвращаем 0
    def get_weight(self, vertex1, vertex2):
        for vert in self.matrix[vertex1]:
            if vert[0] == vertex2:
                return vert[1]

        return 0

    def update_amount(self):
        self.vertex_amount += 2
        self.matrix.append([])
        self.matrix.append([])


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def round(self):
        return Point(int(self.x), int(self.y))

    def __add__(self, other):
        if type(other) == int:
            return Point(self.x + other, self.y + other)
        else:
            return Point(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        if type(other) == int:
            return Point(self.x - other, self.y - other)
        else:
            return Point(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __str__(self):
        return "{},{}".format(self.x, self.y)

    def __hash__(self):
        return self.x.__hash__() ^ self.y.__hash__()


class Segment:
    def __init__(self, start, end):
        # start, end - объекты класса Point
        self.start = start
        self.end = end

    def reverse(self):
        return Segment(self.end, self.start)

    def round(self):
        return Segment(self.start.round(), self.end.round())
    
    def __eq__(self, another):
        return self.start == another.start and self.end == another.end or self.end == another.start and self.start == another.end

    def __getitem__(self, key):
        if not key in [0, 1]:
            raise IndexError
        
        return self.start if key == 0 else self.end

    def __str__(self):
        return "[{}, {}]".format(self.start, self.end)
