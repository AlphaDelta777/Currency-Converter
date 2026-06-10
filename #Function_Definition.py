# Function Definitions (with 'def' keyword)

def calculate_rectangle_area(length, width):
    """Calculates the area of a rectangle"""
    area = length * width
    return area

def calculate_circle_area(radius):
    """Calculates the area of a circle"""
    pi = 3.14159
    area = pi * radius ** 2
    return area

def calculate_triangle_area(base, height):
    """Calculates the area of a triangle"""
    area = 0.5 * base * height
    return area

def calculate_square_area(side):
    """Calculates the area of a square"""
    area = side * side
    return area 

if __name__ == "__main__":
    print(calculate_rectangle_area(5, 3))
    print(calculate_circle_area(4))
    print(calculate_triangle_area(6, 8))
    print(calculate_square_area(4))
