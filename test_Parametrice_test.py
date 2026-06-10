import pytest
from Parametrize_test import grade

@pytest.mark.parametrize("score, expected", [

    (95, "A"), (85, "B"), (75, "C"), (65, "D"), (55, "F"), (100, "A"), (0, "F"),
    (90, "A"), (80, "B"), (70, "C"), (60, "D"), (59, "F"),

    (-1, ValueError), 
    (-4, ValueError),
    (-100, ValueError),
    (-0.5, ValueError),

    (101, ValueError), 
    (259, ValueError),
    (9999, ValueError),
    (100.1, ValueError),

    ('A', ValueError),
    ('aa', ValueError),
    ('xyz', ValueError),
    ('100%', ValueError)
])
def test_all_grade_cases(score, expected):
    """A single test function capturing all normal outputs and validating global exclusions."""
    if expected == ValueError:
        with pytest.raises(ValueError):
            grade(score)
    else:
        assert grade(score) == expected