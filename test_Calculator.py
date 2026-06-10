import pytest
from Calculator import Calculator

@pytest.fixture
def sample_numbers():
    return {"a": 10, "b": 5}


def test_add_positive_numbers(sample_numbers):
    assert Calculator.add(sample_numbers["a"], sample_numbers["b"]) == 15

def test_add_returns_float_when_needed():
    assert Calculator.add(1.5, 2.5) == pytest.approx(4.0)


def test_add_with_zero():
    assert Calculator.add(0, 5) == 5

def test_add_negative_numbers():
    assert Calculator.add(-3, -7) == -10


def test_divide_by_zero_raises():
    with pytest.raises(ZeroDivisionError):
        Calculator.divide(10, 0)