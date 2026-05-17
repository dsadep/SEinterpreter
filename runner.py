from converter import Converter
from parser import Parser
from tokens import Tokeniser


class Runner:
    @staticmethod
    def run():
        while True:
            try:
                expression = input('>>> ')
                converted = Converter.convert(expression)
                tokens = Tokeniser.tokenise(converted)
                parser = Parser(tokens)
                print(parser.expression())
            except Exception as e:
                print(e.with_traceback(None))
                continue