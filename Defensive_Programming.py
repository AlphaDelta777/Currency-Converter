class Rectangle:
    def __init__(self, width, height):
        if width <= 0 or height <= 0:
            raise ValueError("Width and height must be positive.")
        self.width = width
        self.height = height

    def set_width(self, width):
        if width <= 0:
            raise ValueError("Width must be positive.")
        self.width = width

    def set_height(self, height):
        if height <= 0:
            raise ValueError("Height must be positive.")
        self.height = height

    def get_area(self):
        return self.width * self.height

    def get_perimeter(self):
        return 2 * (self.width + self.height)

    def scale(self, factor):
        if factor <= 0:
            raise ValueError("Scale factor must be positive.")
        self.width *= factor
        self.height *= factor


if __name__ == "__main__": 
 
    r = Rectangle(4, 6)
    print("Area:", r.get_area())          
    print("Perimeter:", r.get_perimeter())  


    r.scale(2)
    print("Scaled area:", r.get_area())     


    tests = [
        lambda: Rectangle(-1, 5),
        lambda: Rectangle(5, 0),
        lambda: Rectangle("abc", 10),
        lambda: r.set_width(0),
        lambda: r.set_height("hello"),
        lambda: r.scale(-3),
    ]

    for test in tests:
        try:
            test()
        except Exception as e:
            print("Error:", e)
