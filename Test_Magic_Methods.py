import pytest
from Magic_Methods import Vector 

def test_vector_initialization():
    v = Vector(3, 5)
    assert v.x == 3
    assert v.y == 5

def test_vector_addition():
    v1 = Vector(1, 2)
    v2 = Vector(3, 4)
    result = v1 + v2
    assert result == Vector(4, 6)

def test_vector_equality():
    v1 = Vector(1, 2)
    v2 = Vector(1, 2)
    v3 = Vector(3, 4)
    assert v1 == v2
    assert v1 != v3

def test_vector_string_representation():
    v = Vector(1, 2)
    assert str(v) == "Vector(1, 2)"

def test_vector_dot_product_operator():
    v1 = Vector(1, 2)
    v2 = Vector(3, 4)
    assert v1 @ v2 == 11

def test_vector_dot_product_method():
    v1 = Vector(1, 2)
    v2 = Vector(3, 4)
    assert v1.dot(v2) == 11

def test_dot_product_with_zero_vector():
    v1 = Vector(5, 5)
    zero_v = Vector(0, 0)
    assert v1 @ zero_v == 0
    