
from math_utils import MathUtils


def test_add():
    math = MathUtils()
    assert math.add(2, 3) == 5
    assert math.add(-1, 1) == 0


def test_subtract():
    math = MathUtils()
    assert math.subtract(5, 3) == 2
    assert math.subtract(0, 5) == -5

def test_multiply():
    math = MathUtils()
    assert math.multiply(4, 3) == 12
    assert math.multiply(0, 10) == 0

def test_divide():
    math = MathUtils()
    assert math.divide(10, 2) == 5
    assert math.divide(5, 0) == -1.0
