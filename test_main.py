import pytest

from handler.converter import Converter
from handler.evaluator import Evaluator
from handler.parser import Parser
from handler.tokens import Tokeniser




def evaluate(expression):
    converted = Converter.convert(expression)
    tokens = Tokeniser.tokenise(converted)
    parser = Parser(tokens)
    evaluator = Evaluator()
    return evaluator.eval(parser.expression())

class TestUnary:
    def test_unary_minus_simple(self):
        assert evaluate('-2') == -2

    # def test_unary_minus_float(self):
    #     assert evaluate('-3.0') == -3.0

    def test_unary_plus(self):
        assert evaluate('+5') == 5

    def test_double_unary_minus(self):
        assert evaluate('--2') == 2

    def test_triple_unary_minus(self):
        assert evaluate('---2') == -2

    def test_unary_minus_in_addition(self):
        assert evaluate('1 + -2') == -1

    def test_unary_minus_in_multiplication(self):
        assert evaluate('2 * -3') == -6

    def test_unary_minus_with_parentheses(self):
        assert evaluate('-(1 + 2)') == -3

    def test_unary_minus_nested_parens(self):
        assert evaluate('-(-2)') == 2

    def test_unary_minus_complex(self):
        assert evaluate('-(2 + 3) * 2') == -10

    def test_unary_minus_before_factor_in_term(self):
        assert evaluate('10 + -2 * 3') == 4

    def test_unary_minus_applied_to_paren_expression(self):
        assert evaluate('2 * -(3 + 4)') == -14



class TestPower:
    def test_simple_power(self):
        assert evaluate('2 ^ 3') == 8

    def test_power_of_one(self):
        assert evaluate('5 ^ 1') == 5

    def test_power_of_zero(self):
        assert evaluate('5 ^ 0') == 1

    def test_zero_to_power(self):
        assert evaluate('0 ^ 5') == 0

    def test_right_associativity(self):
        assert evaluate('2 ^ 3 ^ 2') == 512

    def test_power_with_multiplication(self):
        assert evaluate('2 * 3 ^ 2') == 18

    def test_power_with_addition(self):
        assert evaluate('1 + 2 ^ 3') == 9

    def test_unary_minus_and_power(self):
        assert evaluate('-2 ^ 3') in (-8, -8)

    def test_power_in_parens(self):
        assert evaluate('(2 ^ 3) ^ 2') == 64

    def test_power_and_paren_order(self):
        assert evaluate('2 ^ (3 + 1)') == 16



class TestComparison:
    def test_less_than_true(self):
        assert evaluate('1 < 2') == True

    def test_less_than_false(self):
        assert evaluate('2 < 1') == False

    def test_less_or_equal_equal(self):
        assert evaluate('2 <= 2') == True

    def test_less_or_equal_less(self):
        assert evaluate('1 <= 2') == True

    def test_less_or_equal_greater(self):
        assert evaluate('3 <= 2') == False

    def test_greater_than_true(self):
        assert evaluate('5 > 3') == True

    def test_greater_than_false(self):
        assert evaluate('1 > 3') == False

    def test_greater_or_equal_equal(self):
        assert evaluate('3 >= 3') == True

    def test_greater_or_equal_greater(self):
        assert evaluate('4 >= 3') == True

    def test_greater_or_equal_less(self):
        assert evaluate('2 >= 3') == False

    def test_comparison_with_arithmetic_left(self):
        assert evaluate('1 + 2 < 5') == True

    def test_comparison_with_arithmetic_both(self):
        assert evaluate('2 * 3 > 1 + 4') == True

    def test_comparison_with_parens(self):
        assert evaluate('(2 + 3) >= 5') == True

    def test_comparison_with_unary(self):
        assert evaluate('-1 < 0') == True

    def test_comparison_with_power(self):
        assert evaluate('2 ^ 3 > 7') == True



class TestEquality:
    def test_equal_numbers_true(self):
        assert evaluate('1 == 1') == True

    def test_equal_numbers_false(self):
        assert evaluate('1 == 2') == False

    def test_not_equal_true(self):
        assert evaluate('1 != 2') == True

    def test_not_equal_false(self):
        assert evaluate('1 != 1') == False

    def test_equality_with_arithmetic(self):
        assert evaluate('1 + 2 == 3') == True

    def test_equality_arithmetic_both_sides(self):
        assert evaluate('2 * 3 == 3 * 2') == True

    def test_equality_with_comparison(self):
        # (1 < 2) == True
        assert evaluate('(1 < 2) == 1') == True

    def test_inequality_arithmetic(self):
        assert evaluate('2 + 2 != 5') == True

    def test_equality_with_power(self):
        assert evaluate('2 ^ 3 == 8') == True

    def test_equality_with_unary(self):
        assert evaluate('-3 == -3') == True

    def test_equality_negative_and_positive(self):
        assert evaluate('-1 != 1') == True

class TestLogicalAnd:
    def test_true_and_true(self):
        assert evaluate('1 and 1')

    def test_true_and_false(self):
        assert not evaluate('1 and 0')

    def test_false_and_true(self):
        assert not evaluate('0 and 1')

    def test_false_and_false(self):
        assert not evaluate('0 and 0')

    def test_and_with_comparison(self):
        assert evaluate('1 < 2 and 3 > 1')

    def test_and_with_comparison_false(self):
        assert not evaluate('1 < 2 and 3 < 1')

    def test_and_with_equality(self):
        assert evaluate('1 == 1 and 2 == 2')

    def test_and_priority_over_or(self):
        assert evaluate('0 or 1 and 1')

    def test_and_chain(self):
        assert evaluate('1 and 1 and 1')

    def test_and_chain_with_zero(self):
        assert not evaluate('1 and 0 and 1')

    def test_and_with_arithmetic(self):
        assert evaluate('(2 + 2 == 4) and (3 * 3 == 9)')

    def test_and_with_unary(self):
        assert evaluate('-1 < 0 and 1 > 0')

    def test_and_with_nested_parens(self):
        assert evaluate('(1 + 2 == 3) and (4 - 1 == 3)')


class TestLogicalOr:
    def test_true_or_true(self):
        assert evaluate('1 or 1')

    def test_true_or_false(self):
        assert evaluate('1 or 0')

    def test_false_or_true(self):
        assert evaluate('0 or 1')

    def test_false_or_false(self):
        assert not evaluate('0 or 0')

    def test_or_with_comparison(self):
        assert evaluate('5 < 1 or 1 < 5')

    def test_or_with_equality(self):
        assert evaluate('1 == 2 or 2 == 2')

    def test_or_chain(self):
        assert evaluate('0 or 0 or 1')

    def test_or_chain_all_false(self):
        assert not evaluate('0 or 0 or 0')

    def test_or_with_arithmetic(self):
        assert evaluate('2 + 2 == 5 or 2 + 2 == 4')

    def test_or_with_and_precedence(self):
        assert evaluate('1 or 0 and 0')

    def test_or_complex(self):
        assert evaluate('(1 == 2 or 2 == 2) and (3 > 1 or 5 < 1)')


class TestComplex:
    def test_full_arithmetic(self):
        assert evaluate('(1 + 2 * 3 - 4) / (5 - 4)') == 3

    def test_power_inside_comparison(self):
        assert evaluate('2 ^ 10 > 1000') == True

    def test_unary_in_comparison(self):
        assert evaluate('-5 + 3 < 0') == True

    def test_nested_parens_arithmetic(self):
        assert evaluate('((2 + 3) * (4 - 1)) / 5') == 3

    def test_comparison_and_equality(self):
        assert evaluate('(1 < 2) == 1') == True

    def test_double_comparison_in_and(self):
        assert evaluate('1 < 2 and 2 < 3 and 3 < 4') == True

    def test_or_of_comparisons(self):
        assert evaluate('5 < 1 or 1 < 5 or 3 == 3') == True

    def test_deep_nesting_logical(self):
        assert evaluate('(1 + 1 == 2) and (2 * 2 == 4) or (5 == 6)') == True

    def test_unary_and_comparison(self):
        assert evaluate('(-1 + 3) > 1 and (2 ^ 2) == 4') == True

    def test_power_with_comparison_and_logical(self):
        assert evaluate('2 ^ 3 == 8 and 3 ^ 2 == 9') == True

    def test_complex_or_and_chain(self):
        assert evaluate('(0 == 1 or 1 == 1) and (2 + 2 == 4 or 3 + 3 == 7)') == True

    def test_arithmetic_both_sides_of_equality_in_and(self):
        assert evaluate('2 * 5 == 10 and 12 / 4 == 3') == True

    def test_unary_double_minus_in_expression(self):
        assert evaluate('--2 + --3 == 5') == True

    def test_unary_applied_to_expression_in_comparison(self):
        assert evaluate('-(2 + 3) == -5') == True

    def test_large_complex_expression(self):
        assert evaluate('((1 + 2) * (3 ^ 2) - 4) > 20 and (0 or 1)') == True


class TestErrors:
    def test_division_by_zero(self):
        with pytest.raises(ZeroDivisionError):
            evaluate('10 / 0')

    def test_division_by_zero_expression(self):
        with pytest.raises(ZeroDivisionError):
            evaluate('10 / (5 - 5)')

    def test_missing_closing_paren(self):
        with pytest.raises(SyntaxError):
            evaluate('(1-1')