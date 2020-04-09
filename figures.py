class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


    def __add__(self, other):
        self.x += other.x
        self.y += other.y
    
    
    def __sub__(self, other):
        self.x -= other.x
        self.y -= other.y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    
    def __str__(self):
        return "({}, {})".format(self.x, self.y)


class Segment:
    def __init__(self, start, end):
        # start, end - объекты класса Point
        self.start = start
        self.end = end
    
    def __str__(self):
        return "({}, {})".format(self.start, self.end)


class Polygon:
    def __init__(self, points=[]):
        self.points = points


    def add_point_xy(self, x, y):
        self.points.append(Point(x, y))

    def add_point_p(self, point):
        self.points.append(point)


    def inp(self, point):
        return point in self.points


    def __getitem__(self, key):
        return self.points[key]

    
    def __len__(self):
        return len(self.points)
    

    def __iter__(self):
        self.it = 0
        return self   


    def __next__(self):
        if self.it >= len(self.points):
            raise StopIteration   
         
        self.it += 1
        return self.points[self.it - 1]

    
    def __str__(self):
        for p in self.points:
            yield p
