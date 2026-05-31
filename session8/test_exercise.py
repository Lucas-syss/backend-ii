from exercise import multiply


def test_multiply_positive_integers():
    assert multiply(3, 4) == 12


def test_multiply_by_zero():
    assert multiply(0, 99) == 0


def test_multiply_negative():
    assert multiply(-2, 5) == -10


def test_multiply_two_negatives():
    assert multiply(-3, -4) == 12


def test_multiply_floats():
    assert multiply(2.5, 4) == 10.0
