from pkg.calculator import Calculator


def test_addition():
    calc = Calculator()
    assert calc.evaluate("3 + 5") == 8


def test_subtraction():
    calc = Calculator()
    assert calc.evaluate("10 - 4") == 6


def test_multiplication():
    calc = Calculator()
    assert calc.evaluate("3 * 4") == 12


def test_division():
    calc = Calculator()
    assert calc.evaluate("10 / 2") == 5


def test_nested_expression():
    calc = Calculator()
    assert calc.evaluate("3 * 4 + 5") == 17


def test_complex_expression():
    calc = Calculator()
    assert calc.evaluate("2 * 3 - 8 / 2 + 5") == 7


def test_empty_expression():
    calc = Calculator()
    assert calc.evaluate("") is None


def test_invalid_operator():
    calc = Calculator()
    import pytest
    with pytest.raises(ValueError):
        calc.evaluate("$ 3 5")


def test_not_enough_operands():
    calc = Calculator()
    import pytest
    with pytest.raises(ValueError):
        calc.evaluate("+ 3")
