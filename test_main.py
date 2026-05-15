import pytest

from main import Converter, Tokeniser, Parser


def evaluate(expr: str):
    converted = Converter.convert(expr)
    tokens = Tokeniser.tokenise(converted)
    parser = Parser(tokens)
    return parser.evaluate()


# ---------- Converter ----------

def test_converter_empty_string():
    assert Converter.convert('') == ['EOF']


def test_converter_only_spaces():
    assert Converter.convert('   ') == ['EOF']


def test_converter_one_number():
    assert Converter.convert('7') == [7, 'EOF']


def test_converter_multi_digit_number():
    assert Converter.convert('123') == [123, 'EOF']


def test_converter_simple_expression():
    assert Converter.convert('12 + 3') == [12, '+', 3, 'EOF']


def test_converter_expression_with_parentheses():
    assert Converter.convert('(12 + 3)') == ['(', 12, '+', 3, ')', 'EOF']


def test_converter_nested_parentheses():
    assert Converter.convert('((2+3)*4)') == ['(', '(', 2, '+', 3, ')', '*', 4, ')', 'EOF']


# ---------- Tokeniser ----------

def test_tokeniser_number():
    tokens = Tokeniser.tokenise([12, 'EOF'])
    assert tokens[0]['type'] == 'NUM'
    assert tokens[0]['value'] == 12
    assert tokens[1]['type'] == 'EOF'


def test_tokeniser_add():
    tokens = Tokeniser.tokenise(['+', 'EOF'])
    assert tokens[0]['type'] == 'ADD'
    assert tokens[0]['value'] == '+'
    assert tokens[1]['type'] == 'EOF'


def test_tokeniser_parentheses():
    tokens = Tokeniser.tokenise(['(', 2, ')', 'EOF'])
    assert [tok['type'] for tok in tokens] == ['LPAREN', 'NUM', 'RPAREN', 'EOF']
    assert [tok['value'] for tok in tokens] == ['(', 2, ')', 'EOF']


def test_tokeniser_full_sequence():
    tokens = Tokeniser.tokenise(['(', 12, '+', 3, ')', '*', 2, 'EOF'])
    assert [tok['type'] for tok in tokens] == [
        'LPAREN', 'NUM', 'ADD', 'NUM', 'RPAREN', 'MUL', 'NUM', 'EOF'
    ]


# ---------- Simple evaluation ----------

def test_eval_number_only():
    assert evaluate('5') == 5


def test_eval_add():
    assert evaluate('1 + 2') == 3


def test_eval_sub():
    assert evaluate('7 - 4') == 3


def test_eval_mul():
    assert evaluate('2 * 3') == 6


def test_eval_div():
    assert evaluate('8 / 2') == 4


def test_eval_spaces():
    assert evaluate('  12   +   3  ') == 15


def test_eval_multi_digit():
    assert evaluate('123 + 7') == 130


# ---------- Priority without parentheses ----------

def test_eval_priority_mul_before_add():
    assert evaluate('1 + 2 * 3') == 7


def test_eval_priority_mul_before_sub():
    assert evaluate('10 - 2 * 3') == 4


def test_eval_priority_left_to_right_same_level_mul_div():
    assert evaluate('20 / 5 * 2') == 8


def test_eval_priority_left_to_right_same_level_add_sub():
    assert evaluate('10 - 3 - 2') == 5


def test_eval_priority_mixed():
    assert evaluate('8 / 2 + 3 * 2') == 10


# ---------- Parentheses ----------

def test_eval_single_parenthesized_number():
    assert evaluate('(2)') == 2


def test_eval_simple_parentheses():
    assert evaluate('(1 + 2)') == 3


def test_eval_parentheses_change_priority():
    assert evaluate('(1 + 2) * 3') == 9


def test_eval_parentheses_right_side():
    assert evaluate('2 * (3 + 4)') == 14


def test_eval_nested_parentheses():
    assert evaluate('((2 + 3) * 4)') == 20


def test_eval_double_nested_parentheses():
    assert evaluate('2 * ((1 + 2) * (3 + 1))') == 24


def test_eval_parentheses_inside_parentheses():
    assert evaluate('(2 + (3 * 4))') == 14


def test_eval_complex_expression():
    assert evaluate('((12 + 3) * 2 - 4) / 2') == 13


# ---------- Error cases ----------

def test_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        evaluate('10 / 0')


def test_division_by_zero_in_parentheses():
    with pytest.raises(ZeroDivisionError):
        evaluate('10 / (5 - 5)')


def test_missing_closing_parenthesis():
    with pytest.raises(SyntaxError):
        evaluate('(1 + 2')


def test_extra_closing_parenthesis():
    with pytest.raises(SyntaxError):
        evaluate('1 + 2)')


def test_nested_missing_closing_parenthesis():
    with pytest.raises(SyntaxError):
        evaluate('((1 + 2) * 3')


def test_empty_parentheses():
    with pytest.raises(SyntaxError):
        evaluate('()')


def test_operator_at_end():
    with pytest.raises(Exception):
        evaluate('1 +')


def test_operator_at_start():
    with pytest.raises(Exception):
        evaluate('* 2')


def test_two_operators_in_row():
    with pytest.raises(Exception):
        evaluate('1 ++ 2')


def test_invalid_character():
    with pytest.raises(Exception):
        evaluate('2 + a')