from handler.converter import Converter
from handler.evaluator import Evaluator
from handler.parser import Parser
from handler.tokens import Tokeniser


class Runner:
    @staticmethod
    def run():
        while True:
            try:
                expression = input('>>> ')
                converted = Converter.convert(expression)
                tokens = Tokeniser.tokenise(converted)
                parser = Parser(tokens)
                evaluator = Evaluator()
                result = evaluator.eval(parser.expression())
                print(result)
            except Exception as e:
                print(e.with_traceback(None))
                continue