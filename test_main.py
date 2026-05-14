from converter import Converter
from tokens import Tokeniser
from parser import Parser


def eval_expr(expr: str):
    converted = Converter.convert(expr)
    tokens = Tokeniser.tokenise(converted)
    parser = Parser(tokens)
    return parser.expression()


def test_converter_empty():
    assert Converter.convert('') == ['EOF']


def test_converter_spaces():
    assert Converter.convert('   ') == ['EOF']


def test_converter_one_number():
    assert Converter.convert('7') == [7, 'EOF']


def test_converter_multi_digit():
    assert Converter.convert('123') == [123, 'EOF']


def test_converter_simple_expression():
    assert Converter.convert('12 + 3') == [12, '+', 3, 'EOF']


def test_converter_ignore_spaces():
    assert Converter.convert('  12   +   3  ') == [12, '+', 3, 'EOF']


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


def test_tokeniser_sequence():
    tokens = Tokeniser.tokenise([12, '+', 3, 'EOF'])
    assert [t['type'] for t in tokens] == ['NUM', 'ADD', 'NUM', 'EOF']
    assert [t['value'] for t in tokens] == [12, '+', 3, 'EOF']


def test_eval_add():
    assert eval_expr('1 + 2') == 3


def test_eval_sub():
    assert eval_expr('7 - 4') == 3


def test_eval_mul():
    assert eval_expr('2 * 3') == 6


def test_eval_div():
    assert eval_expr('8 / 2') == 4


def test_eval_priority_1():
    assert eval_expr('1 + 2 * 3') == 7


def test_eval_priority_2():
    assert eval_expr('10 - 2 * 3') == 4


def test_eval_priority_3():
    assert eval_expr('20 / 5 * 2') == 8


def test_eval_multi_digit():
    assert eval_expr('12 + 34') == 46


def test_eval_spaces():
    assert eval_expr('  12   +  3 * 2 ') == 18