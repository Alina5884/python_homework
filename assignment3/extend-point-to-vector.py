class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    def __str__(self):
        return "Point({}, {})".format(self.x, self.y)
    def distance_to(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        return (dx*dx + dy*dy) ** 0.5

class Vector(Point):
    def __str__(self):
        return "<{}, {}>".format(self.x, self.y)
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

p1 = Point(1, 2)
p2 = Point(4, 6)
print(p1)
print(p2)
print("Equal?", p1 == p2)
print("Distance:", p1.distance_to(p2))

v1 = Vector(1, 1)
v2 = Vector(2, 3)
print(v1)
print(v2)
print("v1 + v2 =", v1 + v2)
print("Vector equals same coords:", v1 == Vector(1, 1))