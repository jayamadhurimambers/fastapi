import pytest
from typehint import Calculator

class TestCalculator:
    def setup_method(self):
        calc = Calculator()

    def test_function1_case1(self):
        assert self.calc.function1(2, 3) == 5

    def test_function1_case2(self):
        assert self.calc.function1(5, 3) == 8

    def test_function2_case1(self):
        assert self.calc.function2(2, 3) == 6

    def test_function2_case2(self):
        assert self.calc.function2(5, 3) == 15


