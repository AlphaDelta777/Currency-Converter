class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __matmul__(self, other):
        return (self.x * other.x) + (self.y * other.y)
    
    def dot(self, other):
        return (self.x * other.x) + (self.y * other.y)
    
    def __str__(self):
        return f"Vector({self.x}, {self.y})"
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

v1 = Vector(1, 2)
v2 = Vector(3, 4)


v3 = v1 + v2  
print(f"Addition: {v3}")      

dot_operator = v1 @ v2          
print(f"Dot (via @): {dot_operator}") 


dot_method = v1.dot(v2)          
print(f"Dot (via method): {dot_method}") 