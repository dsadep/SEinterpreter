from converter import Converter
from parser import Parser
from tokens import Tokeniser

    
if __name__ == '__main__':
    expression = input('Input regular expression:\n')
    tokens = Tokeniser.tokenise(Converter.convert(expression))
    print(tokens)
    parser = Parser(tokens)
    print(parser.evaluate())
    