from Defensive_Programming import Rectangle

def test_valid_initialization():
    r = Rectangle(4, 6)
    print("test_valid_initialization passed")

def test_invalid_initialization_negative():
    try:
        Rectangle(-1, 5)
    except ValueError:
        print("test_invalid_initialization_negative passed")

def test_invalid_initialization_zero():
    try:
        Rectangle(5, 0)
    except ValueError:
        print("test_invalid_initialization_zero passed")

def test_invalid_initialization_non_numeric():
    try:
        Rectangle("abc", 10)
    except TypeError:
        print("test_invalid_initialization_non_numeric passed")

def test_set_width_valid():
    r = Rectangle(4, 6)
    r.set_width(10)
    print("test_set_width_valid passed")

def test_set_width_invalid():
    r = Rectangle(4, 6)
    try:
        r.set_width(0)
    except ValueError:
        print("test_set_width_invalid passed")

def test_set_height_valid():
    r = Rectangle(4, 6)
    r.set_height(8)
    print("test_set_height_valid passed")

def test_set_height_invalid():
    r = Rectangle(4, 6)
    try:
        r.set_height(-3)
    except ValueError:
        print("test_set_height_invalid passed")

def test_set_height_non_numeric():
    r = Rectangle(4, 6)
    try:
        r.set_height("hello")
    except TypeError:
        print("test_set_height_non_numeric passed")

def test_area():
    r = Rectangle(4, 6)
    assert r.get_area() == 24
    print("test_area passed")

def test_perimeter():
    r = Rectangle(4, 6)
    assert r.get_perimeter() == 20
    print("test_perimeter passed")

def test_scale_valid():
    r = Rectangle(4, 6)
    r.scale(2)
    assert r.width == 8 and r.height == 12
    print("test_scale_valid passed")

def test_scale_invalid():
    r = Rectangle(4, 6)
    try:
        r.scale(-3)
    except ValueError:
        print("test_scale_invalid passed")


if __name__ == "__main__": # pragma: no cover
    test_valid_initialization()
    test_invalid_initialization_negative()
    test_invalid_initialization_zero()
    test_invalid_initialization_non_numeric()
    test_set_width_valid()
    test_set_width_invalid()
    test_set_height_valid()
    test_set_height_invalid()
    test_set_height_non_numeric()
    test_area()
    test_perimeter()
    test_scale_valid()
    test_scale_invalid()
