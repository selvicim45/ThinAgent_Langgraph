from project import add,sub,mul,div
def test_add():
    assert add.invoke({'num1': 2, 'num2': 3}) == 5
    assert add.invoke({'num1': -1, 'num2': 1}) == 0
    assert add.invoke({'num1': 0, 'num2': 0}) == 0

def test_sub():
    assert sub.invoke({'num1': 5, 'num2': 3}) == 2
    assert sub.invoke({'num1': 2, 'num2': 3}) == -1
    assert sub.invoke({'num1': 0, 'num2': 0}) == 0

def test_mul():
    assert mul.invoke({'num1': 4, 'num2': 5}) == 20
    assert mul.invoke({'num1': -2, 'num2': 3}) == -6
    assert mul.invoke({'num1': 0, 'num2': 10}) == 0

def test_div():
    assert div.invoke({'num1': 10, 'num2': 2}) == 5
    assert div.invoke({'num1': 7, 'num2': 1}) == 7
    try:
        div.invoke({'num1': 5, 'num2': 0})
    except ValueError as e:
        assert str(e) == "Division by zero is not allowed. Please enter a non-zero denominator."
    else:
        assert False, "div(5, 0) did not raise ValueError"

def test_div_zero_pytest():
    import pytest
    with pytest.raises(ValueError):
        div.invoke({'num1': 3, 'num2': 0})
