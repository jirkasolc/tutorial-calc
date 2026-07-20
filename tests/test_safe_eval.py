import pytest
from calculator import safe_eval


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("1+1", 2.0),
        ("2*3+1", 7.0),
        ("(2+3)*4", 20.0),
        ("-5+10", 5.0),
    ],
)
def test_safe_eval_basic(expr, expected):
    assert safe_eval(expr) == expected


def test_safe_eval_reject_large_exponent():
    with pytest.raises(ValueError):
        safe_eval("2**1000")


def test_safe_eval_unsupported_node():
    with pytest.raises(ValueError):
        safe_eval("__import__('os').system('echo hi')")
