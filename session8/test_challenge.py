import pytest
from challenge import factorial


@pytest.mark.parametrize("n,expected", [
    (0, 1),
    (1, 1),
    (2, 2),
    (3, 6),
    (4, 24),
    (5, 120),
    (6, 720),
    (10, 3628800),
])
def test_factorial(n, expected):
    assert factorial(n) == expected


def test_factorial_negative_raises():
    with pytest.raises(ValueError):
        factorial(-1)


def test_factorial_large_negative_raises():
    with pytest.raises(ValueError):
        factorial(-100)
