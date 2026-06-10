from lecture1 import fizzBuzz


def test_fizzbuzz_basic():
    assert fizzBuzz(1) == ["1"]


def test_fizzbuzz_fizz():
    assert fizzBuzz(3) == ["1", "2", "Fizz"]


def test_fizzbuzz_buzz():
    assert fizzBuzz(5) == ["1", "2", "Fizz", "4", "Buzz"]


def test_fizzbuzz_fizzbuzz():
    assert fizzBuzz(15) == [
        "1", "2", "Fizz", "4", "Buzz",
        "Fizz", "7", "8", "Fizz", "Buzz",
        "11", "Fizz", "13", "14", "FizzBuzz",
    ]
